import os
import random
import string
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'deception-secret-key-123'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent', ping_timeout=60)

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

rooms = {}

@app.route('/')
def index():
    return render_template('index.html')

def get_lobby_data(room_code):
    if room_code not in rooms: return {'players': [], 'host': None}
    room = rooms[room_code]
    return {
        'players': [{'name': p['name'], 'uid': uid, 'online': p['online']} for uid, p in room['players'].items()],
        'host': room['host_uid']
    }

@socketio.on('create_room')
def handle_create(data):
    uid = data['uid']
    name = data['name']
    
    room_code = ''.join(random.choices(string.ascii_uppercase, k=4))
    while room_code in rooms:
        room_code = ''.join(random.choices(string.ascii_uppercase, k=4))
        
    rooms[room_code] = {
        'status': 'waiting',
        'host_uid': uid,
        'players': {},
        'murderer_data': {'weapon': None, 'clue': None, 'ready': False},
        'active_tiles': [],
        'deck_tiles': [],
        'discarded_tiles': [],
        'tile_selections': {},
        'replace_count': 2
    }
    
    join_room(room_code)
    rooms[room_code]['players'][uid] = {'name': name, 'sid': request.sid, 'role': None, 'means': [], 'clues': [], 'online': True}
    
    emit('room_joined', {'room_code': room_code, 'uid': uid, 'is_host': True}, to=request.sid)
    emit('update_lobby', get_lobby_data(room_code), to=room_code)

@socketio.on('join_room')
def handle_join(data):
    uid = data['uid']
    name = data['name']
    room_code = data['room_code'].upper()
    
    if room_code not in rooms:
        emit('error', {'msg': 'রুম কোডটি ভুল বা গেমটি আর নেই! নতুন রুম তৈরি করুন।', 'clear_storage': True}, to=request.sid)
        return
        
    room = rooms[room_code]
    
    if uid not in room['players'] and room['status'] != 'waiting':
        emit('error', {'msg': 'এই রুমে অলরেডি গেম চলছে! এখন জয়েন করা যাবে না।', 'clear_storage': True}, to=request.sid)
        return
        
    join_room(room_code)
    
    if uid not in room['players']:
        room['players'][uid] = {'name': name, 'sid': request.sid, 'role': None, 'means': [], 'clues': [], 'online': True}
    else:
        room['players'][uid]['sid'] = request.sid
        room['players'][uid]['online'] = True
        
    if not room['host_uid'] or room['host_uid'] not in room['players']:
        room['host_uid'] = uid
        
    is_host = (room['host_uid'] == uid)
    emit('room_joined', {'room_code': room_code, 'uid': uid, 'is_host': is_host}, to=request.sid)
    emit('update_lobby', get_lobby_data(room_code), to=room_code)
    
    if room['status'] != 'waiting':
        recover_game_state(room_code, uid, request.sid)

# --- রুম থেকে বের হওয়ার নতুন ইভেন্ট ---
@socketio.on('leave_room_event')
def handle_leave_room(data):
    uid = data.get('uid')
    room_code = data.get('room_code')
    
    if room_code in rooms and uid in rooms[room_code]['players']:
        leave_room(room_code) # সকেট রুম থেকে বের করা
        del rooms[room_code]['players'][uid] # প্লেয়ার লিস্ট থেকে বাদ দেওয়া
        
        # যদি হোস্ট বের হয়ে যায়, তবে অন্য কাউকে হোস্ট বানানো
        if rooms[room_code]['host_uid'] == uid:
            if len(rooms[room_code]['players']) > 0:
                rooms[room_code]['host_uid'] = list(rooms[room_code]['players'].keys())[0]
            else:
                del rooms[room_code] # রুমে কেউ না থাকলে রুম ডিলিট
                return
                
        emit('update_lobby', get_lobby_data(room_code), to=room_code)

def recover_game_state(room_code, uid, sid):
    room = rooms[room_code]
    p = room['players'][uid]
    if not p['role']: return
    
    emit('game_started', {'role': p['role'], 'means': p['means'], 'clues': p['clues']}, to=sid)
    
    if room['status'] == 'playing':
        public_data = {
            'players': [{'name': v['name'], 'role': 'বিজ্ঞানী' if v['role']=='ফরেনসিক বিজ্ঞানী' else 'player', 'means': v['means'], 'clues': v['clues']} for k, v in room['players'].items()],
            'active_tiles': room['active_tiles'],
            'discarded_tiles': room['discarded_tiles'],
            'tile_selections': room['tile_selections'],
            'replace_count': room['replace_count']
        }
        if p['role'] == 'ফরেনসিক বিজ্ঞানী':
            murderer_name = next(v['name'] for k, v in room['players'].items() if v['role'] == 'খুনি')
            emit('investigation_started', {
                **public_data, 
                'secret': {
                    'murderer': murderer_name, 
                    'weapon': room['murderer_data']['weapon'], 
                    'clue': room['murderer_data']['clue']
                }
            }, to=sid)
        else:
            emit('investigation_started', public_data, to=sid)

@socketio.on('start_game')
def handle_start(data):
    room_code = data['room_code']
    room = rooms[room_code]
    
    if request.sid != room['players'][room['host_uid']]['sid']: return
    
    uids = list(room['players'].keys())
    if len(uids) < 4:
        emit('error', {'msg': 'কমপক্ষে ৪ জন প্লেয়ার দরকার!'}, to=request.sid)
        return
        
    room['status'] = 'selecting'
    room['murderer_data'] = {'weapon': None, 'clue': None, 'ready': False}
    room['tile_selections'] = {}
    
    roles = ["খুনি", "ফরেনসিক বিজ্ঞানী", "তদন্তকারী", "তদন্তকারী"]
    for i in range(4, len(uids)): roles.append("তদন্তকারী")
    if len(uids) >= 6: roles[roles.index("তদন্তকারী")] = "সহযোগী"
    if len(uids) >= 8: roles[roles.index("তদন্তকারী")] = "সাক্ষী"
    
    random.shuffle(roles)
    shuffled_means = random.sample(meansDB, len(meansDB))
    shuffled_clues = random.sample(cluesDB, len(cluesDB))
    
    for i, uid in enumerate(uids):
        role = roles[i]
        room['players'][uid]['role'] = role
        if role != "ফরেনসিক বিজ্ঞানী":
            room['players'][uid]['means'] = [shuffled_means.pop() for _ in range(4)]
            room['players'][uid]['clues'] = [shuffled_clues.pop() for _ in range(4)]
        else:
            room['players'][uid]['means'] = []
            room['players'][uid]['clues'] = []
            
        emit('game_started', {'role': role, 'means': room['players'][uid]['means'], 'clues': room['players'][uid]['clues']}, to=room['players'][uid]['sid'])

@socketio.on('murderer_selected')
def handle_murderer_selection(data):
    room_code = data['room_code']
    room = rooms[room_code]
    uid = data['uid']
    
    if room['players'][uid]['role'] != 'খুনি': return
    room['murderer_data'] = {'weapon': data['weapon'], 'clue': data['clue'], 'ready': True}
    
    room['status'] = 'playing'
    cause_tile = next(t for t in sceneDB if t['id'] == 'cause')
    loc_tiles = [t for t in sceneDB if t['id'].startswith('loc')]
    other_tiles = [t for t in sceneDB if not t['isRequired']]
    
    random.shuffle(loc_tiles)
    random.shuffle(other_tiles)
    
    room['active_tiles'] = [cause_tile, loc_tiles[0], other_tiles[0], other_tiles[1], other_tiles[2], other_tiles[3]]
    room['deck_tiles'] = other_tiles[4:]
    room['discarded_tiles'] = []
    room['replace_count'] = 2
    
    for sid_data in room['players'].values():
        recover_game_state(room_code, next(k for k,v in room['players'].items() if v==sid_data), sid_data['sid'])

@socketio.on('update_tile_selection')
def handle_tile_update(data):
    room_code = data['room_code']
    room = rooms[room_code]
    uid = data['uid']
    
    if room['players'][uid]['role'] == 'ফরেনসিক বিজ্ঞানী':
        room['tile_selections'][data['tile_id']] = data['value']
        emit('tile_updated', data, to=room_code, include_self=False)

@socketio.on('replace_tile')
def handle_replace_tile(data):
    room_code = data['room_code']
    room = rooms[room_code]
    uid = data['uid']
    
    if room['players'][uid]['role'] != 'ফরেনসিক বিজ্ঞানী': return
    if room['replace_count'] <= 0 or len(room['deck_tiles']) == 0: return
    
    tile_id = data['tile_id']
    for i, t in enumerate(room['active_tiles']):
        if t['id'] == tile_id:
            old_tile_name = t['name']
            room['discarded_tiles'].append(old_tile_name)
            
            new_tile = room['deck_tiles'].pop(0)
            room['active_tiles'][i] = new_tile
            room['replace_count'] -= 1
            
            emit('tile_replaced', {
                'old_tile': old_tile_name,
                'active_tiles': room['active_tiles'],
                'discarded_tiles': room['discarded_tiles'],
                'replace_count': room['replace_count']
            }, to=room_code)
            break

@socketio.on('reset_game')
def handle_reset(data):
    room_code = data['room_code']
    room = rooms[room_code]
    uid = data['uid']
    
    if uid != room['host_uid']: return
    
    room['status'] = 'waiting'
    room['murderer_data'] = {'weapon': None, 'clue': None, 'ready': False}
    room['active_tiles'] = []
    room['deck_tiles'] = []
    room['discarded_tiles'] = []
    room['tile_selections'] = {}
    room['replace_count'] = 2
    
    for player_uid in room['players']:
        room['players'][player_uid]['role'] = None
        room['players'][player_uid]['means'] = []
        room['players'][player_uid]['clues'] = []
        
    emit('back_to_lobby', get_lobby_data(room_code), to=room_code)

@socketio.on('disconnect')
def handle_disconnect():
    for room_code, room in list(rooms.items()):
        for uid, p in list(room['players'].items()):
            if p.get('sid') == request.sid:
                p['online'] = False
                
                if room['status'] == 'waiting':
                    del room['players'][uid]
                    if room['host_uid'] == uid:
                        if room['players']:
                            room['host_uid'] = list(room['players'].keys())[0]
                        else:
                            del rooms[room_code]
                            return
                
                emit('update_lobby', get_lobby_data(room_code), to=room_code)
                return

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
