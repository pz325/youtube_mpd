import requests
import argparse
import urlparse
import xml.dom.minidom

parser = argparse.ArgumentParser(description='Youtube DASH MPD parser')
parser.add_argument('--url', '-u', required=True)
parser.add_argument('--output', '-o')

args = parser.parse_args()


parsed = urlparse.urlparse(args.url)
video_id = urlparse.parse_qs(parsed.query)['v'][0]
print('Youtube video id: {video_id}'.format(video_id=video_id))

video_info_url = 'https://www.youtube.com/get_video_info?el=info&ps=default&video_id={video_id}&hl=en&sts=17316&gl=US&eurl='.format(video_id=video_id)
print('Youtube video info url: {video_info_url}'.format(video_info_url=video_info_url))

r = requests.get(video_info_url, verify=False)

dashmpd_url = urlparse.parse_qs(r.content)['dashmpd'][0]
print('Youtube DASH MPD URL: {dashmpd_url}'.format(dashmpd_url=dashmpd_url))


r = requests.get(dashmpd_url, verify=False)

if args.output:
    f = open(args.output, 'w')
    f.write(r.content)
    f.close()
else:
    print('==== Youtube DASH MPD ====')
    xml = xml.dom.minidom.parseString(r.content)
    print(xml.toprettyxml())
