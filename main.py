from PIL.Image import NONE
import streamlit as st
from streamlit.callbacks import websocket
from streamlit_flowide import LiveMap
import re
import json
import random

mapConfig = {
}

WEBSOCKET_URL = ""

path_pattern = re.compile("\/(tag\.[0-9]+)\/([a-zA-Z]+)")

colors = ['red','blue','lime','orange','gold','violet','black']

FORKLIFT_ICON = "icons/map-pin-icon-hand-cart.svg"




st.set_page_config(layout='wide')

button = st.empty()

start = button.button('Start')

stop = None

ctx = LiveMap(mapConfig)



st.session_state.tags = set()
def ws_handler(buffer):

    if stop:
        st.stop()   
    for patches in buffer:
        for patch in json.loads(patches):
            matches = path_pattern.match(patch["path"])   
            tag = matches.group(1)
            var = matches.group(2)
            if var != 'position':
                continue
            if tag not in st.session_state.tags:
                ctx.create_marker(tag,patch["value"],scale=0.8)
                ctx.change_main_color(tag,random.choice(colors))
                ctx.change_main_icon(tag,FORKLIFT_ICON)
                st.session_state.tags.add(tag)
            else:
                ctx.move_marker(tag,patch["value"])




if start:
    websocket.on_message_buffered(f"{WEBSOCKET_URL}/v2/locations/websocket",ws_handler,1,key="ws")
    stop = button.button("Stop")
