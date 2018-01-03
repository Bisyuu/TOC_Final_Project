from transitions import State
from transitions.extensions import GraphMachine as Machine

class StateMachine(Machine):
    pass

states = [
    {'name': 'Set_service'},
    {'name': 'Search_image'},
    {'name': 'Search_wiki'},
    {'name': 'Search_gamewith'},
    {'name': 'Set_element'},
    {'name': 'Set_character'},
    {'name': 'Set_level'}
]

transitions = [
    ['Image_set','Set_service','Search_image'],
    ['Wiki_set','Set_service','Search_wiki'],
    ['Gamewith_set','Set_service','Search_gamewith'],
    ['Element_SELECT',['Search_image','Search_wiki','Search_gamewith'],'Set_element'],
    ['Element_OK','Set_element','Set_character'],
    ['Element_REDO','Set_character','Set_element'],
    ['Character_OK','Set_character','Set_level'],
    ['Character_REDO','Set_level','Set_character'],
    ['Level_OK','Set_level','Set_service'],
    ['Reset',['Set_element','Set_character','Set_level'],'Set_service']
]
