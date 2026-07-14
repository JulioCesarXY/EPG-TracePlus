import requests
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Mapeamento definitivo e único com as URLs reais do Umbraco
CANAIS = [
    ("Trace Toca", "TRACE_TOCA", "TOCA", "https://media.umbraco.io/trace-backoffice/aisj3x2s/01_2024_trace-_eng_tv-channels-logos-with-zone-inclusion_trace-toca_-angola-c-verde-mozambique_1200x800_v1.jpg"),
    ("Trace Brazuca", "TRACE_BRAZUCA", "BRAZIL", "https://media.umbraco.io/trace-backoffice/srvpyki2/01_2024_trace-_pt_tv-channels-logos-with-zone-inclusion_trace-brasil-brasil__1200x800_v1.png"),
    ("Trace Urban SA", "TRACE_URBAN_SA", "URBAN_SA", "https://media.umbraco.io/trace-backoffice/iuidd41o/01_2024_trace-_eng_tv-channels-logos-with-zone-inclusion_trace-urban-southern-africa_1200x800_v1.jpg"),
    ("Trace Naija", "TRACE_NAIJA", "NAIJA", "https://media.umbraco.io/trace-backoffice/rkyl1h4s/01_2024_trace-_eng_tv-channels-logos-with-zone-inclusion_trace-naija-nigeria_1200x800_v1.jpg"),
    ("Trace Ivoire", "TRACE_IVOIRE", "TRACE_IVOIRE", "https://media.umbraco.io/trace-backoffice/bf1boec4/logo_traceplus_trace-ivoire_eng_color_rgb.png"),
    ("Trace Mziki", "TRACE_MZIKI", "MZIKI", "https://media.umbraco.io/trace-backoffice/pssjpwr5/01_2024_trace-_eng_tv-channels-logos-with-zone-inclusion_trace-mziki-east-africa_1200x800_v1.jpg"),
    ("Trace Africa EN", "TRACE_AFRICA_EN", "AFRICA_EN", "https://media.umbraco.io/trace-backoffice/m5thaean/01_2024_trace-_eng_tv-channels-logos-with-zone-inclusion_trace-gospel-nigeria-east-africa_1200x800_v1.jpg"),
    ("Trace Jama", "TRACE_JAMA", "JAMA", "https://media.umbraco.io/trace-backoffice/wx4cscwp/01_2024_trace-_eng_tv-channels-logos-with-zone-inclusion_trace-jama-ghana_1200x800_v1.jpg"),
    ("Trace UK", "TRACE_UK", "UK_FAST", "https://media.umbraco.io/trace-backoffice/lu0blq2l/01_2024_trace-_eng_tv-channels-logos-with-zone-inclusion_trace-uk-united-kingdom_1200x800_v1.jpg"),
    ("Trace Gospel SA", "TRACE_GOSPEL_SA", "GOSPEL_SA", "https://media.umbraco.io/trace-backoffice/u5kjb4ra/01_2024_trace-_eng_tv-channels-logos-with-zone-inclusion_trace-gospel-southern-africa_1200x800_v1.jpg"),
    ("Trace Muzika", "TRACE_MUZICA", "MUZIKA", "https://media.umbraco.io/trace-backoffice/bhljdj0m/01_2024_trace-_eng_tv-channels-logos-with-zone-inclusion_trace-muzika-ethiopia_1200x800_v1.jpg"),
    ("Trace Urban Inter", "TRACE_URBAN_INT", "URBAN_INTER", "https://media.umbraco.io/trace-backoffice/gbvclgv4/01_2024_trace-_eng_tv-channels-logos-with-zone-inclusion_trace-urban-international_1200x800_v1.jpg"),
    ("Trace Caribbean", "TRACE_CARIBBEAN", "CARIBBEAN", "https://media.umbraco.io/trace-backoffice/qluekida/01_2024_trace-_eng_tv-channels-logos-with-zone-inclusion_trace-caribbean-caribbean_1200x800_v1.jpg"),
    ("Trace Latina", "TRACE_LATINA", "LATINA", "https://media.umbraco.io/trace-backoffice/gssla4u2/01_2024_trace-_eng_tv-channels-logos-with-zone-inclusion_trace-latina-latin-america_1200x800_v1.jpg"),
    ("Trace Gospel FR", "TRACE_GOSPEL_FR", "GOSPEL_FR", "https://media.umbraco.io/trace-backoffice/0nfbllov/01_2024_trace-_eng_tv-channels-logos-with-zone-inclusion_trace-gospel-africa-franco_1200x800_v1.jpg"),
    ("Trace Ayiti", "TRACE_AYITI", "AYITI", "https://media.umbraco.io/trace-backoffice/a2yep4va/01_2024_trace-_eng_tv-channels-logos-with-zone-inclusion_trace-ayiti-haiti_1200x800_v1.jpg"),
    ("Trace Kitoko", "TRACE_KITOKO", "KITOKO", "https://media.umbraco.io/trace-backoffice/t3iav1hu/01_2024_trace-_eng_tv-channels-logos-with-zone-inclusion_trace-kitoko-congo_1200x800_v1.png"),
    ("Trace Gospel ROA", "TRACE_GOSPEL_ROA", "GOSPEL_ROA", "https://media.umbraco.io/trace-backoffice/wvyotsas/2025_tngo_channel_logo_traceplus_eng_1200x800.png"),
    ("Trace Mboa", "TRACE_MBOA", "MBOA", "https://media.umbraco.io/trace-backoffice/su4mcbo3/01_2024_trace-_eng_tv-channels-logos-with-zone-inclusion_trace-mboa-cameroon_1200x800_v1.jpg"),
    ("Trace Africa FR", "TRACE_AFRICA", "AFRICA_FR", "https://media.umbraco.io/trace-backoffice/55qdwsip/01_2024_trace-_eng_tv_channels_logos_with_zone_inclusion_trace_africa_-_francophone_1200x800_v1-1.jpg"),
    ("Trace Urban Afr FR", "TRACE_URBAN_AFR_FR", "URBAN_AFRIC_FR", "https://media.umbraco.io/trace-backoffice/k1kj3mr4/01_2024_trace-_eng_tv-channels-logos-with-zone-inclusion_trace-urban-africa-franco_1200x800_v1.jpg"),
    ("Trace Vanilla", "TRACE_VANILLA", "VANILLA", "https://media.umbraco.io/trace-backoffice/opupyuil/01_2024_trace-_eng_tv-channels-logos-with-zone-inclusion_trace-vanilla-indian-ocean_1200x800_v1.jpg"),
    ("Trace Urban FR", "TRACE_URBAN_FR", "URBAN_FR", "https://media.umbraco.io/trace-backoffice/5i4pv1b1/01_2024_trace-_eng_tv-channels-logos-with-zone-inclusion_trace-urban-france_1200x800_v1.jpg"),
    ("Trace Teranga", "TRACE_AFRIKORA", "TERANGA", "https://media.umbraco.io/trace-backoffice/chbdvrsx/01_2024_trace-_eng_tv-channels-logos-with-zone-inclusion_trace-teranga_senegal-mail-gambia_1200x800_v1.jpg"),
    ("Trace Sports", "TRACE_SPORTS", "TRACE_SPORT_STARS", "https://media.umbraco.io/trace-backoffice/ttibw1u5/01_2024_trace-_eng_tv-channels-logos-with-zone-inclusion_trace-sports-sports-celebrities_1200x800_v1.jpg"),
    ("Trace Urban Dom", "TRACE_URBAN_DOM", "URBAN_DOM", "https://media.umbraco.io/trace-backoffice/r3mklqsu/01_2024_trace-_eng_tv-channels-logos-with-zone-inclusion_trace-urban-caribbean-indian-ocean_1200x800_v1.jpg")
]

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"

def clean_xmltv_date(date_str):
    if not date_str:
        return ""
    clean_num = date_str.replace('-', '').replace(':', '').replace('T', '')
    base_time = clean_num.split('.')[0][:14]
    return f"{base_time} +0000"

def build_m3u():
    print("Gerando lista M3U com logos limpas do Umbraco...")
    m3u_lines = ["#EXTM3U\n"]
    for nome, tvg_id, slug_stream, logo_url in CANAIS:
        stream_url = f"https://channels.trace.plus/Traceprod/{slug_stream}/abr.m3u8"
        
        m3u_lines.append(f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{nome}" tvg-logo="{logo_url}" group-title="Trace Network",{nome}')
        m3u_lines.append(f'#EXTVLCOPT:http-user-agent={USER_AGENT}')
        m3u_lines.append('#EXTVLCOPT:http-referrer=https://trace.plus/')
        m3u_lines.append(f"{stream_url}\n")
        
    with open("canais_trace.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_lines))
    print("Arquivo 'canais_trace.m3u' atualizado com sucesso!")

def build_merged_epg():
    print("Iniciando mesclagem e normalização de datas...")
    root_master = ET.Element('tv', generator_info_name="Trace-Master-Pipeline")
    
    for nome, tvg_id, _, logo_url in CANAIS:
        channel_elem = ET.SubElement(root_master, 'channel', id=tvg_id)
        ET.SubElement(channel_elem, 'display-name').text = nome
        ET.SubElement(channel_elem, 'icon', src=logo_url)

    for nome, tvg_id, _, _ in CANAIS:
        epg_url = f"https://filesapp.trace.tv/files/epg/export/{tvg_id}/epg.xml"
        if tvg_id in ["TRACE_IVOIRE", "TRACE_URBAN_FR"]:
            epg_url = epg_url.replace("https://", "http://")
            
        try:
            response = requests.get(epg_url, headers={"User-Agent": USER_AGENT}, timeout=10)
            if response.status_code == 200:
                xml_text = re.sub(r'\sxmlns="[^"]+"', '', response.text, count=1)
                try:
                    tree = ET.fromstring(xml_text.encode('utf-8'))
                    program_count = 0
                    for elem in tree.iter():
                        if elem.tag.split('}')[-1] == 'programme':
                            elem.set('channel', tvg_id)
                            elem.set('start', clean_xmltv_date(elem.get('start')))
                            elem.set('stop', clean_xmltv_date(elem.get('stop')))
                            root_master.append(elem)
                            program_count += 1
                    print(f"-> {nome}: {program_count} programas importados.")
                except ET.ParseError:
                    print(f"-> Erro de sintaxe XML em {nome}.")
            else:
                print(f"-> Falha em {nome} (Status: {response.status_code})")
        except Exception as e:
            print(f"-> Erro em {nome}: {e}")

    print("Salvando arquivo mestre...")
    raw_xml = ET.tostring(root_master, encoding='utf-8')
    pretty_xml = minidom.parseString(raw_xml).toprettyxml(indent="  ")
    with open("epg_final.xml", "w", encoding="utf-8") as f:
        f.write(pretty_xml)
    print("Arquivo 'epg_final.xml' gerado com sucesso!")

if __name__ == "__main__":
    build_m3u()
    print("-" * 40)
    build_merged_epg()
