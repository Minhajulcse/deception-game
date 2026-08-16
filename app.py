import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'deception-secret-key-123'

# Render-এর জন্য Eventlet এবং CORS কনফিগারেশন
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet', ping_timeout=60)

# গেমের ডাটাবেস
meansDB = ["মদ / অ্যালকোহল", "অ্যামিবা বা জীবাণু", "আর্সেনিক", "অগ্নিসংযোগ", "কুড়াল", "বাঁশ", "ক্রিকেট ব্যাট", "চামড়ার বেল্ট", "কামড়ানো ও ছিঁড়ে ফেলা", "ধারালো অস্ত্র", "ব্লেন্ডার", "অতিরিক্ত রক্তক্ষরণ", "এন্টিকাটার", "ইট", "জীবন্ত কবর দেওয়া", "মোমবাতি দানি", "চেইনস", "চাপাতি", "ক্রাচ", "ছোরা", "দূষিত পানি", "অঙ্গচ্ছেদ", "ড্রিল মেশিন", "পানিতে ডোবানো", "ডাম্বেল", "ই-বাইক", "ইলেকট্রিক ব্যাটন", "বৈদ্যুতিক শক", "বিস্ফোরক", "ফোল্ডিং চেয়ার", "বন্দুক", "হাতুড়ি", "লোহার আংটা", "আইস স্কেটস", "অবৈধ মাদক", "ইনজেকশন", "কেরোসিন", "লাথি", "চাকু", "লাইটার ফ্লুইড", "রামদা", "মেশিনগান", "পাগলা কুকুর", "দেশলাই", "পারদ", "লোহার শিকল", "জিআই তার", "ওভারডোজ", "কস্টেপ", "কীটনাশক", "ঘুমের বড়ি", "বালিশ", "পিস্তল", "মহামারী", "পলিথিন ব্যাগ", "বিষাক্ত তীর", "বিষাক্ত গ্যাস", "বিষাক্ত সুই", "টবের গাছ", "পাউডার", "ঘুষি", "ধাক্কা দেওয়া", "তেজস্ক্রিয় বিকিরণ", "রেজর ব্লেড", "রশি / দড়ি", "ওড়না", "কাঁচি", "ভাস্কর্য", "গুলি করা", "স্নাইপার রাইফেল", "অনাহার", "লোহার রড", "পাথর", "এসিড", "তলোয়ার", "টেজার", "গামছা", "ট্রফি", "খুরপি", "খালি হাত", "বিষাক্ত বিচ্ছু", "বিষধর সাপ", "গেম কনসোল", "ভাইরাস", "চাবুক", "ওয়াইন", "ইলেকট্রিক তার", "কাঠের টুকরো", "বুট জুতো", "রেঞ্চ"]
cluesDB = ["আপেল", "ব্যাজ", "ব্যান্ডেজ", "টাকার নোট", "ঘণ্টা", "রক্ত", "হাড়", "বই", "ব্রেসলেট", "পাউরুটি", "ব্রিফকেস", "ঝাড়ু", "গুলির খোসা", "বোতাম", "কেক", "ক্যালেন্ডার", "চকলেট", "বেত", "ক্যাসেট টেপ", "বিড়াল", "মোবাইল ফোন", "চক", "চুরুট", "সিগারেটের ছাই", "সিগারেটের ফিল্টার", "পরিষ্কার করার ন্যাকড়া", "ঘড়ি", "কাপড়চোপড়", "কোস্টার", "কয়েন", "কমিক বই", "কম্পিউটার", "সিডি/ডিভিডি", "কম্পিউটার মাউস", "কন্টাক্ট লেন্স", "কসমেটিকস", "তুলা", "চায়ের কাপ", "পর্দা", "নকল দাঁত", "হীরা", "ডায়েরি", "ডিকশনারি", "কাদা", "নথিপত্র", "কুকুর", "ধুলা", "কানের দুল", "কেঁচো", "খাম", "পরীক্ষার খাতা", "কুরিয়ারের প্যাকেট", "ফ্যান", "পালক", "সুতা", "নখ", "আঙুলের ছাপ", "বাঁশি", "লিফলেট", "খাবার", "পায়ের ছাপ", "কাঁটাচামচ", "নষ্ট বাল্ব", "গিয়ার", "উপহার", "চশমা", "গ্লাভস", "আঠা", "চুল", "চুলের ক্লিপ", "চিরুনি", "হাতকড়া", "রুমাল", "পেনড্রাইভ", "টুপি", "হেডফোন", "হেলমেট", "আইডি কার্ড", "বরফ", "আইসক্রিম", "কালি", "পোকা", "ব্রডব্যান্ড তার", "দাওয়াত কার্ড", "জ্যাকেট", "গহনা", "জুস", "চাবি", "গাছের পাতা", "চামড়া", "চামড়ার জুতা", "ক্যামেরার লেন্স", "চিঠি", "লাইটার", "লিপস্টিক", "তালা", "লটারির টিকিট", "প্রেমের চিঠি", "সুটকেস", "টিফিন বক্স", "ম্যাগাজিন", "আতশ কাঁচ", "মানচিত্র", "মাস্ক", "দেশলাইয়ের কাঠি", "ঔষধ", "রেস্টুরেন্টের মেনু", "মাইক্রোফোন", "আয়না", "স্মার্টফোন", "খেলনা গাড়ি", "মশার কয়েল", "পেরেক", "গলার হার", "সুই", "পত্রিকা", "চিরকুট", "খাতা", "নাট-বল্টু", "তেল", "রং", "অন্তর্বাস", "পাসপোর্ট", "পাসওয়ার্ড", "বাদাম", "কলম", "পার্স", "প্লাস্টিকের বোতল", "সিরাপ"]

sceneDB = [
    {"id": "cause", "name": "মৃত্যুর কারণ (বাধ্যতামূলক)", "isRequired": True, "options": ["-সিলেক্ট করুন-", "শ্বাসরোধ", "গুরুতর আঘাত", "অতিরিক্ত রক্তক্ষরণ", "অসুস্থতা / রোগ", "বিষক্রিয়া", "দুর্ঘটনা"]},
    {"id": "loc1", "name": "অপরাধের স্থান (ক)", "isRequired": True, "options": ["-সিলেক্ট করুন-", "বসার ঘর", "শোবার ঘর", "গুদাম ঘর", "বাথরুম", "রান্নাঘর", "বারান্দা"]},
    {"id": "loc2", "name": "অপরাধের স্থান (খ)", "isRequired": True, "options": ["-সিলেক্ট করুন-", "রিসোর্ট / গ্রামের বাড়ি", "পার্ক", "সুপারমার্কেট", "স্কুল", "জঙ্গল", "ব্যাংক"]},
    {"id": "loc3", "name": "অপরাধের স্থান (গ)", "isRequired": True, "options": ["-সিলেক্ট করুন-", "পাব / বার", "লাইব্রেরি", "রেস্টুরেন্ট", "হোটেল", "হাসপাতাল", "নির্মাণাধীন ভবন"]},
    {"id": "t1", "name": "ঘটনাস্থলের অবস্থা", "isRequired": False, "options": ["-সিলেক্ট করুন-", "টুকরো টুকরো", "ছাই", "পানির দাগ", "ফাটল বা ভাঙাচোরা", "এলোমেলো", "গোছানো"]},
    {"id": "t2", "name": "মৃত্যুর সময়", "isRequired": False, "options": ["-সিলেক্ট করুন-", "ভোর", "সকাল", "দুপুর", "বিকেল", "সন্ধ্যা", "মধ্যরাত"]},
    {"id": "t3", "name": "আবহাওয়া", "isRequired": False, "options": ["-সিলেক্ট করুন-", "রৌদ্রোজ্জ্বল", "বৃষ্টি", "বজ্রপাত", "মেঘলা", "কুয়াশাচ্ছন্ন", "ঝড়ো হাওয়া"]},
    {"id": "t4", "name": "ঘটনাস্থলে চিহ্ন", "isRequired": False, "options": ["-সিলেক্ট করুন-", "পায়ের ছাপ", "রক্ত", "মাটি / কাদা", "তরল পদার্থ", "আঁচড়ের দাগ", "চুল"]},
    {"id": "t5", "name": "নিহতের অভিব্যক্তি", "isRequired": False, "options": ["-সিলেক্ট করুন-", "শান্ত", "ধস্তাধস্তি", "ভীত", "যন্ত্রণাকাতর", "শূন্যদৃষ্টি", "রাগান্বিত"]},
    {"id": "t6", "name": "আকস্মিক ঘটনা", "isRequired": False, "options": ["-সিলেক্ট করুন-", "লোডশেডিং", "আগুন", "মারামারি", "চুরি", "চিৎকার", "কিছুই না"]},
    {"id": "t7", "name": "যা চলছিল", "isRequired": False, "options": ["-সিলেক্ট করুন-", "বিনোদন", "বিশ্রাম", "আড্ডা / জমায়েত", "কেনাবেচা", "বেড়াতে আসা", "খাওয়া-দাওয়া"]},
    {"id": "t8", "name": "নিহতের শারীরিক গঠন", "isRequired": False, "options": ["-সিলেক্ট করুন-", "বিশাল", "মোটা", "সাধারণ", "শুকনা", "ছোটখাটো", "শিশু"]},
    {"id": "t9", "name": "নিহতের পোশাক", "isRequired": False, "options": ["-সিলেক্ট করুন-", "পরিপাটি", "অগোছালো", "দামি", "ছেঁড়াফাটা", "অদ্ভুত", "নগ্ন"]},
    {"id": "t10", "name": "লাশে পাওয়া সূত্র", "isRequired": False, "options": ["-সিলেক্ট করুন-", "মাথা", "বুক", "হাত", "পা", "আংশিক", "সারা শরীর"]},
    {"id": "t11", "name": "খুনির ব্যক্তিত্ব", "isRequired": False, "options": ["-সিলেক্ট করুন-", "অহংকারী", "জঘন্য", "রাগী", "লোভী", "বলপ্রয়োগকারী", "বিকৃতমনা"]},
    {"id": "t12", "name": "হত্যার উদ্দেশ্য", "isRequired": False, "options": ["-সিলেক্ট করুন-", "শত্রুতা", "ক্ষমতা", "টাকা", "প্রেম", "ঈর্ষা", "বিচার / প্রতিশোধ"]},
    {"id": "t13", "name": "নিহতের পরিচয়", "isRequired": False, "options": ["-সিলেক্ট করুন-", "শিশু", "তরুণ", "মধ্যবয়সী", "বৃদ্ধ", "পুরুষ", "মহিলা"]},
    {"id": "t14", "name": "নিহতের পেশা", "isRequired": False, "options": ["-সিলেক্ট করুন-", "মালিক", "চাকরিজীবী", "শ্রমিক", "ছাত্র", "বেকার", "অবসরপ্রাপ্ত"]},
    {"id": "t15", "name": "সাধারণ ধারণা", "isRequired": False, "options": ["-সিলেক্ট করুন-", "সাধারণ", "প্রান্তিক", "আনুষ্ঠানিক", "ঠান্ডা", "গরম", "আকর্ষণীয়"]}
]

game_state = {
    'status': 'waiting',
    'players': {}, 
    'host_sid': None,
    'murderer_data': {'weapon': None, 'clue': None, 'ready': False},
    'active_tiles': [],
    'deck_tiles': [],
    'replace_count': 2
}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join_game')
def handle_join(data):
    name = data['name']
    
    if not game_state['host_sid'] or game_state['host_sid'] not in game_state['players']:
        game_state['host_sid'] = request.sid

    game_state['players'][request.sid] = {
        'name': name,
        'role': None,
        'means': [],
        'clues': [],
        'ready': False
    }
    
    emit('update_lobby', get_lobby_data(), broadcast=True)

def get_lobby_data():
    return {
        'players': [{'name': p['name'], 'sid': sid} for sid, p in game_state['players'].items()],
        'host': game_state['host_sid']
    }

@socketio.on('start_game')
def handle_start():
    if request.sid != game_state['host_sid']:
        return
    
    player_sids = list(game_state['players'].keys())
    count = len(player_sids)
    if count < 4:
        emit('error', {'msg': 'কমপক্ষে ৪ জন প্লেয়ার দরকার! বন্ধুদের জয়েন করতে বলুন।'}, to=request.sid)
        return
        
    game_state['status'] = 'selecting'
    game_state['murderer_data'] = {'weapon': None, 'clue': None, 'ready': False}
    
    roles = ["খুনি", "ফরেনসিক বিজ্ঞানী", "তদন্তকারী", "তদন্তকারী"]
    for i in range(4, count): roles.append("তদন্তকারী")
    if count >= 6: roles[roles.index("তদন্তকারী")] = "সহযোগী"
    if count >= 8: roles[roles.index("তদন্তকারী")] = "সাক্ষী"
    
    random.shuffle(roles)
    shuffled_means = random.sample(meansDB, len(meansDB))
    shuffled_clues = random.sample(cluesDB, len(cluesDB))
    
    for i, sid in enumerate(player_sids):
        role = roles[i]
        game_state['players'][sid]['role'] = role
        if role != "ফরেনসিক বিজ্ঞানী":
            game_state['players'][sid]['means'] = [shuffled_means.pop() for _ in range(4)]
            game_state['players'][sid]['clues'] = [shuffled_clues.pop() for _ in range(4)]
        else:
            game_state['players'][sid]['means'] = []
            game_state['players'][sid]['clues'] = []
            
        emit('game_started', {'role': role, 'means': game_state['players'][sid]['means'], 'clues': game_state['players'][sid]['clues']}, to=sid)

@socketio.on('murderer_selected')
def handle_murderer_selection(data):
    if game_state['players'][request.sid]['role'] != 'খুনি': return
    game_state['murderer_data'] = {'weapon': data['weapon'], 'clue': data['clue'], 'ready': True}
    start_investigation()

def start_investigation():
    game_state['status'] = 'playing'
    cause_tile = next(t for t in sceneDB if t['id'] == 'cause')
    loc_tiles = [t for t in sceneDB if t['id'].startswith('loc')]
    other_tiles = [t for t in sceneDB if not t['isRequired']]
    
    random.shuffle(loc_tiles)
    random.shuffle(other_tiles)
    
    game_state['active_tiles'] = [cause_tile, loc_tiles[0], other_tiles[0], other_tiles[1], other_tiles[2], other_tiles[3]]
    game_state['deck_tiles'] = other_tiles[4:]
    game_state['replace_count'] = 2
    
    public_data = {
        'players': [{'name': p['name'], 'role': 'বিজ্ঞানী' if p['role']=='ফরেনসিক বিজ্ঞানী' else 'player', 'means': p['means'], 'clues': p['clues']} for sid, p in game_state['players'].items()],
        'active_tiles': game_state['active_tiles'],
        'replace_count': game_state['replace_count']
    }
    
    for sid, p in game_state['players'].items():
        if p['role'] == 'ফরেনসিক বিজ্ঞানী':
            murderer_name = next(player['name'] for player in game_state['players'].values() if player['role'] == 'খুনি')
            emit('investigation_started', {
                **public_data, 
                'secret': {
                    'murderer': murderer_name, 
                    'weapon': game_state['murderer_data']['weapon'], 
                    'clue': game_state['murderer_data']['clue']
                }
            }, to=sid)
        else:
            emit('investigation_started', public_data, to=sid)

@socketio.on('update_tile_selection')
def handle_tile_update(data):
    if game_state['players'][request.sid]['role'] == 'ফরেনসিক বিজ্ঞানী':
        emit('tile_updated', data, broadcast=True, include_self=False)

@socketio.on('replace_tile')
def handle_replace_tile(data):
    if game_state['players'][request.sid]['role'] != 'ফরেনসিক বিজ্ঞানী': return
    if game_state['replace_count'] <= 0 or len(game_state['deck_tiles']) == 0: return
    
    tile_id = data['tile_id']
    for i, t in enumerate(game_state['active_tiles']):
        if t['id'] == tile_id:
            new_tile = game_state['deck_tiles'].pop(0)
            game_state['active_tiles'][i] = new_tile
            game_state['replace_count'] -= 1
            
            emit('tile_replaced', {
                'old_tile': t['name'],
                'active_tiles': game_state['active_tiles'],
                'replace_count': game_state['replace_count']
            }, broadcast=True)
            break

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in game_state['players']:
        del game_state['players'][request.sid]
        
        if request.sid == game_state['host_sid']:
            game_state['host_sid'] = list(game_state['players'].keys())[0] if game_state['players'] else None
            
        emit('update_lobby', get_lobby_data(), broadcast=True)

if __name__ == '__main__':
    # Render-এর ডাইনামিক পোর্ট রিসিভ করার জন্য
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
