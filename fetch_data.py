import requests
import json
import os

# Konfigurasi API
# URL yang Anda berikan menggunakan domain 1212 (Deli Serdang) dan var 230
API_KEY = os.getenv('BPS_API_KEY')
URL = f"https://webapi.bps.go.id/v1/api/list/model/data/lang/ind/domain/1212/var/230/key/{API_KEY}"

def fetch_bps_data():
    try:
        response = requests.get(URL)
        res_json = response.json()

        if res_json['status'] != 'OK':
            print("Gagal mengambil data dari API BPS")
            return

        # Ambil metadata tahun (vervar) dan jenis kelamin (turvar)
        # BPS menggunakan ID untuk menghubungkan data
        years = res_json['vervar'] # List tahun
        categories = res_json['turvar'] # List Jenis Kelamin (Laki-laki, Perempuan)
        datacontent = res_json['datacontent'] # Isi data asli

        final_data = []

        # Loop setiap tahun yang tersedia di API
        for y in years:
            year_id = str(y['val'])
            year_label = y['label']
            
            # Cari ID untuk Laki-laki dan Perempuan (asumsi ID statis atau cari di turvar)
            # Biasanya ID 1 = Laki-laki, ID 2 = Perempuan dalam var ini
            male_val = 0
            female_val = 0

            for c in categories:
                cat_id = str(c['val'])
                # Key format di BPS: varID + turvarID + vervarID + thID
                # Karena thID sudah masuk di URL (atau dinamis), kita gabungkan kuncinya
                # Format kunci umum BPS: '230' + cat_id + '0' + year_id
                data_key = f"230{cat_id}0{year_id}"
                
                val = datacontent.get(data_key, 0)
                if val == "-" or val is None: val = 0
                
                if "Laki-laki" in c['label']:
                    male_val = int(val)
                elif "Perempuan" in c['label']:
                    female_val = int(val)

            final_data.append({
                "tahun": year_label,
                "male": male_val,
                "female": female_val
            })

        # Urutkan berdasarkan tahun terkecil ke terbesar
        final_data.sort(key=lambda x: x['tahun'])

        # Simpan ke data.json
        with open('data.json', 'w') as f:
            json.dump({"data": final_data}, f, indent=4)
        
        print(f"Berhasil memproses {len(final_data)} tahun data.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    fetch_bps_data()