import requests
import json
import os

API_KEY = os.getenv('BPS_API_KEY')
# Menggunakan URL domain 1212 (Deli Serdang) dan var 230
URL = f"https://webapi.bps.go.id/v1/api/list/model/data/lang/ind/domain/1212/var/230/key/{API_KEY}"

def fetch_bps_data():
    try:
        print("Menghubungi API BPS...")
        response = requests.get(URL)
        res_json = response.json()

        if res_json.get('status') != 'OK':
            print(f"Status API: {res_json.get('status')}")
            return

        vervar = res_json.get('vervar', []) # Tahun
        turvar = res_json.get('turvar', [])   # Jenis Kelamin
        datacontent = res_json.get('datacontent', {})

        result_list = []

        for y in vervar:
            y_id = str(y['val'])
            y_label = y['label']
            
            m_val = 0
            f_val = 0

            for t in turvar:
                t_id = str(t['val'])
                # Format key standar BPS: var + turvar + 0 + vervar
                key = f"230{t_id}0{y_id}"
                val = datacontent.get(key, 0)
                
                # Konversi ke angka, tangani jika data "-"
                try:
                    clean_val = int(val)
                except:
                    clean_val = 0

                if "Laki-laki" in t['label']:
                    m_val = clean_val
                elif "Perempuan" in t['label']:
                    f_val = clean_val

            result_list.append({
                "tahun": y_label,
                "male": m_val,
                "female": f_val
            })

        # Urutkan tahun
        result_list.sort(key=lambda x: x['tahun'])

        # WAJIB: Simpan file
        output = {"data": result_list}
        with open('data.json', 'w') as f:
            json.dump(output, f, indent=4)
        
        print("File data.json berhasil dibuat!")

    except Exception as e:
        print(f"Error fatal: {e}")

if __name__ == "__main__":
    fetch_bps_data()