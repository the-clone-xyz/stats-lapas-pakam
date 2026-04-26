import requests
import json
import os

API_KEY = os.getenv('BPS_API_KEY')
# Gunakan URL yang Anda berikan tadi
URL = f"https://webapi.bps.go.id/v1/api/list/model/data/lang/ind/domain/1212/var/230/key/{API_KEY}"

def fetch_bps_data():
    try:
        response = requests.get(URL)
        res_json = response.json()

        if res_json.get('status') != 'OK':
            print("API BPS mengembalikan status bukan OK")
            return

        vervar = res_json.get('vervar', [])
        turvar = res_json.get('turvar', [])
        datacontent = res_json.get('datacontent', {})

        final_data = []

        for y in vervar:
            y_id = str(y['val'])
            y_label = y['label']
            
            # Cari Laki-laki (biasanya ID 1) dan Perempuan (biasanya ID 2)
            # Kita cari secara dinamis berdasarkan label
            m_val = 0
            f_val = 0

            for t in turvar:
                t_id = str(t['val'])
                # Format key BPS: var_id + turvar_id + vervar_id + th_id
                # Karena URL tidak pakai th_id khusus, formatnya biasanya: var + turvar + 0 + vervar
                key = f"230{t_id}0{y_id}"
                val = datacontent.get(key, 0)
                
                # Bersihkan data jika berupa '-'
                clean_val = int(val) if str(val).isdigit() else 0

                if "Laki-laki" in t['label']:
                    m_val = clean_val
                elif "Perempuan" in t['label']:
                    f_val = clean_val

            final_data.append({"tahun": y_label, "male": m_val, "female": f_val})

        final_data.sort(key=lambda x: x['tahun'])

        with open('data.json', 'w') as f:
            json.dump({"data": final_data}, f, indent=4)
        
        print("Selesai memperbarui data.json")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    fetch_bps_data()