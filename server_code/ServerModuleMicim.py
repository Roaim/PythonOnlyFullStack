import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.media
import json
import os
from datetime import datetime

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

def admin_pass():
  if 'ADMIN_PASS' in os.environ:
    return os.environ['ADMIN_PASS']
  return app_tables.admin.get(key='password')['value']

def admin_secret():
  if 'ADMIN_SECRET' in os.environ:
    return os.environ['ADMIN_SECRET']
  return app_tables.admin.get(key='secret')['value']

def is_valid_token():
  token = anvil.server.session.get('token', encode(admin_secret(),'hello'))
  if token != encode(admin_secret(), admin_pass()):
    return False
  return True

@anvil.server.callable
def check_pass(passwrd):
  retry_count = anvil.server.session.get('retry', 3)
  
  if passwrd == admin_pass() and retry_count > 0:
    anvil.server.session['retry'] = 3
    anvil.server.session['token'] = encode(admin_secret(), passwrd)
    return True
  else:
    retry_count -= 1
    anvil.server.session['retry'] = retry_count
    return False

@anvil.server.callable
def store_json(file):
  json_str = file.get_bytes().decode('UTF-8')
  try:
    json_dict = json.loads(json_str)
    is_ok = True
    if type(json_dict) == list:
      for s in json_dict:
        if type(s) == dict:
          session = s['session']
          videos = s['videos']
          session_row = app_tables.sessions.get(session=session)
          if session_row:
            session_row.delete()
          episode_row = app_tables.episodes.get(session=session)
          if episode_row:
            episode_row.delete()
          app_tables.sessions.add_row(session=session)
          app_tables.episodes.add_row(session=session,episode_list=videos)
        else:
          is_ok = False
    else:
      is_ok = False
    return is_ok
  except:
    return False

  
@anvil.server.callable
def sessions():
  return app_tables.sessions.search()

@anvil.server.callable
def episodes(session):
  return app_tables.episodes.get(session=session)['episode_list']

@anvil.server.callable
def delete_session(session):
  if not is_valid_token():
    return False
  is_success = True
  s = session['session']
  if app_tables.sessions.has_row(session):
    session.delete()
  else:
    is_success = False
  episodes = app_tables.episodes.get(session=s)
  if episodes:
    for e in episodes['episode_list']:
      app_tables.history.add_row(session=s,episode=e,updated=datetime.now())
    episodes.delete()
  else:
    is_success = False
  return is_success

@anvil.server.callable
def delete_episode(session, episodes, episode):
  if not is_valid_token():
    return False
  el = [e for e in episodes if e != episode]
  episode_row = app_tables.episodes.get(session=session)
  if episode_row:
    episode_row['episode_list'] = el
    app_tables.history.add_row(session=session, episode=episode,updated=datetime.now())
  return True

@anvil.server.callable
def histories():
  return [dict(session=h['session'], updated=h['updated'].strftime("%a %d %b, %Y %I:%M:%S %p"), **h['episode']) for h in app_tables.history.search(
    tables.order_by('updated',ascending=False)
  )]

@anvil.server.callable
def clear_history():
  if not is_valid_token():
    return False
  app_tables.history.delete_all_rows()
  return True
  
import base64
def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()
