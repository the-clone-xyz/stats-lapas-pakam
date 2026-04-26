import requests
import json
import os

API_KEY = os.getenv('BPS_API_KEY')
if not API_KEY:
    raise EnvironmentError('API key tidak ditemukan. Set environment variable BPS_API_KEY sebelum menjalankan script.')

# Menggunakan URL domain 1212 (Deli Serdang) dan var 230
URL = f"https://webapi.bps.go.id/v1/api/list/model/data/lang/ind/domain/1212/var/230/th/121/key/{API_KEY}"

def fetch_bps_data():
    try:
        print("Menghubungi API BPS...")
        response = requests.get(URL)
        res_json = response.json()

        if res_json.get('status') != 'OK':
            print(f"Status API: {res_json.get('status')}")
            return

        vervar = res_json.get('vervar', [])  # Bulan
        turvar = res_json.get('turvar', [])   # Jenis Kelamin
        tahun_list = res_json.get('tahun', [])
        turtahun_list = res_json.get('turtahun', [])
        var_list = res_json.get('var', [])
        datacontent = res_json.get('datacontent', {})

        year_id = str(tahun_list[0]['val']) if tahun_list else '0'
        turtahun_id = str(turtahun_list[0]['val']) if turtahun_list else '0'
        var_id = str(var_list[0]['val']) if var_list else '230'

        result_list = []

        for month in vervar:
            month_id = int(month['val'])
            month_label = month['label']
            if month_id <= 3:
                month_code = str(month_id + 9)
            else:
                month_code = str(month_id - 3)

            m_val = 0
            f_val = 0

            for t in turvar:
                t_id = str(t['val'])
                key = f"{month_code}{var_id}{t_id}{year_id}0"
                val = datacontent.get(key, 0)

                # Konversi ke angka, tangani jika data "-"
                try:
                    clean_val = int(val)
                except Exception:
                    clean_val = 0

                if "Laki-laki" in t['label']:
                    m_val = clean_val
                elif "Perempuan" in t['label']:
                    f_val = clean_val

            result_list.append({
                "tahun": month_label,
                "male": m_val,
                "female": f_val
            })

        # WAJIB: Simpan file
        output = {"data": result_list}
        with open('data.json', 'w') as f:
            json.dump(output, f, indent=4)
        
        print("File data.json berhasil dibuat!")

    except Exception as e:
        print(f"Error fatal: {e}")

if __name__ == "__main__":
    fetch_bps_data()