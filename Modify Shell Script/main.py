from flask import Flask, request, jsonify
import logging
import json

app = Flask(__name__)


def apn_parse(apn):
    """Parses the APN string to extract the SIM name and APN value."""
    name = apn.split('[')[1].split(']')[0]
    apn_value = apn.split('=')[1]
    return name, apn_value


@app.route('/to_turn_on', methods=['GET'])
def modify_function():
    sim_name = request.args.get('sim_name')
    apn_name = request.args.get('apn_name')

    if not sim_name or not apn_name:
        return jsonify({"error": "Both sim_name and apn_name must be provided."}), 400

    try:
        with open('/etc/modem_autoconnect.sh', 'r') as main_script:
            raw1 = main_script.read()

        apn_dict = raw1.split('declare -A sim_apn_dict=(\n')[1].split('#enddict')[0].split('\n')
        sims_list = {apn_parse(apn)[0]: apn_parse(apn)[1] for apn in apn_dict if '[' in apn}

        sims_list[f'"{sim_name}"'] = f'"{apn_name}"'

        to_add = '\n    '.join([f'[{key}]={value}' for key, value in sims_list.items()])

        with open('template.sh', 'r') as template:
            template_read = template.read()

        file2 = template_read.replace('#PLACEHERE', to_add)

        with open('/etc/modem_autoconnect.sh', 'w') as after_changes_file:
            after_changes_file.write(file2)

        return jsonify({"message": "The modem_autoconnect.sh file has been successfully modified."}), 200

    except FileNotFoundError as fnf_error:
        logging.error(f"File error: {str(fnf_error)}")
        return jsonify({"error": f"File error: {str(fnf_error)}"}), 500
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route('/remove_apn', methods=['GET'])
def remove_apn_function():
    sim_name = request.args.get('sim_name')

    if not sim_name:
        return jsonify({"error": "sim_name must be provided."}), 400

    try:
        with open('/etc/modem_autoconnect.sh', 'r') as main_script:
            raw1 = main_script.read()

        apn_dict = raw1.split('declare -A sim_apn_dict=(\n')[1].split('#enddict')[0].split('\n')
        sims_list = {apn_parse(apn)[0]: apn_parse(apn)[1] for apn in apn_dict if '[' in apn}

        sims_list.pop(f'"{sim_name}"', None)

        to_add = '\n    '.join([f'[{key}]={value}' for key, value in sims_list.items()])

        with open('template.sh', 'r') as template:
            template_read = template.read()

        file2 = template_read.replace('#PLACEHERE', to_add)

        with open('/etc/modem_autoconnect.sh', 'w') as after_changes_file:
            after_changes_file.write(file2)

        return jsonify({"message": "The specified SIM has been removed successfully."}), 200

    except FileNotFoundError as fnf_error:
        logging.error(f"File error: {str(fnf_error)}")
        return jsonify({"error": f"File error: {str(fnf_error)}"}), 500
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route('/get_apn', methods=['GET'])
def get_apn():
    try:
        with open('/etc/modem_autoconnect.sh', 'r') as main_script:
            raw1 = main_script.read()

        apn_dict = raw1.split('declare -A sim_apn_dict=(\n')[1].split('#enddict')[0].split('\n')
        sims_list = {apn_parse(apn)[0]: apn_parse(apn)[1] for apn in apn_dict if '[' in apn}

        logging.info(f"Returning APN list: {sims_list}")
        return jsonify(sims_list), 200
    except FileNotFoundError as fnf_error:
        logging.error(f"File error: {str(fnf_error)}")
        return jsonify({"error": f"File error: {str(fnf_error)}"}), 500
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route('/read_ethernet', methods=['GET'])
def read_ethernet():
    try:
        with open('/etc/ethernet0_info.txt', 'r') as main_script:
            content = main_script.read().strip()  # Read the entire content and strip extra spaces

            if not content:
                return jsonify({"No Connection": "Ethernet is not connected."}), 200

            list1 = [line.strip() for line in content.splitlines()]

        # Ensure the list has at least 4 lines
        if len(list1) < 4:
            return jsonify({"error": "Invalid content in the ethernet info file."}), 400

        eth_dict = {}
        line2, line3, line4 = list1[1], list1[2], list1[3]

        eth_dict['IP Address'] = line2.split('inet ')[1].split(' ')[0] if 'inet ' in line2 else 'N/A'
        eth_dict['Sub Netmask'] = line2.split('netmask ')[1].split(' ')[0] if 'netmask ' in line2 else 'N/A'
        eth_dict['INET6'] = line3.split('inet6 ')[1].split(' ')[0] if 'inet6 ' in line3 else 'N/A'
        eth_dict['Ether'] = line4.split('ether ')[1].split(' ')[0] if 'ether ' in line4 else 'N/A'

        logging.info(f"Returning Ethernet info: {eth_dict}")
        return jsonify(eth_dict), 200

    except FileNotFoundError as fnf_error:
        logging.error(f"File error: {str(fnf_error)}")
        return jsonify({"error": f"File error: {str(fnf_error)}"}), 500
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(port=5010, host='0.0.0.0')

