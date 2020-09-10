


from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_sdk.forms import FormAction
from typing import Dict, Text, Any, List, Union

import time
import json
import requests

class ActionHandleNo(Action):

    '''
    This implements an action to handle "no" - unfortunately the same
    word is used in English and Spanish for the /deny intent.
    So this action first needs to work out whether "no" is the answer to
    a follow up question or a "no" to the "anything_else" question.
    1. If it's a no to the follow up, then ask anything_else
    2. If it's a no to anything_else, then say goodbye.
    We use slot values and the intent history from the tracker to work
    out where we are.
    '''

    def name(self) -> Text:
        return 'action_handle_no'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        last_intent = tracker.latest_message['intent'].get('name')

        reversed_events = list(reversed(tracker.events))
        user_events = [d for d in reversed_events if d['event'] == 'user']
        # collecting some intents, in case we need them...
        second_last_intent = user_events[1]['parse_data']['intent']['name']
        second_last_intent_confidence = user_events[1]['parse_data']['intent']['confidence']
        third_last_intent = user_events[2]['parse_data']['intent']['name']
        #print(f'Intent chain is {third_last_intent}:{second_last_intent}({second_last_intent_confidence}):{last_intent}')
        #print(f'Intent chain is {third_last_intent}:{second_last_intent}:{last_intent}')

        # if ("pre-follow up in Spanish"):
        if (((tracker.get_slot('cc_life_subtopics_spa') is not None) or (tracker.get_slot('cc_comm_subtopics_spa') is not None)) and
                (not second_last_intent.startswith('affirm'))):
                # We are answering no to an offer of follow up in Spanish
                dispatcher.utter_message(template='utter_anything_else_spa')
                # I don't think clearing these slots here works, it's also done at the end.
                SlotSet('cc_life_subtopics_spa', None)
                SlotSet('cc_comm_subtopics_spa', None)
        # elif ('pre-follow up in English'):
        elif (((tracker.get_slot('cc_life_subtopics_eng') is not None) or (tracker.get_slot('cc_comm_subtopics_eng') is not None)) and
                (not second_last_intent.startswith('affirm'))):
                dispatcher.utter_message(template='utter_anything_else_eng')
        # else, we are answering no to anything else...
        else:
            # if ("speaking Spanish"):
            if (tracker.get_slot('cc_action_topics_spa') is not None) or (tracker.get_slot('cc_comm_subtopics_spa') is not None):
                # We are answering no to anything else in Spanish
                dispatcher.utter_message(template='utter_goodbye_spa')
            else:
                # We are answering no to anything else in English
                dispatcher.utter_message(template='utter_goodbye_eng')

        return [
                # Clear those slots, so that next time we come round, we know to say bye.
                SlotSet('cc_life_subtopics_spa', None),
                SlotSet('cc_comm_subtopics_spa', None),
                SlotSet('cc_life_subtopics_eng', None),
                SlotSet('cc_comm_subtopics_eng', None)
                ]


class ActionSelectFollowUpENG(Action):

    '''
    This (repeated for each language) implements an action to decide if
    there is a follow up question to offer, and if so offer "Want to know more?"
    Follow ups are currently only available for Diet, Advocacy and Education
    Default for all other cases is to ask "anything_else"
    '''

    def name(self) -> Text:
        return 'action_offer_follow_ups_eng'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        last_intent = tracker.latest_message['intent'].get('name')
        print(f'last intent is {last_intent}')

        reversed_events = list(reversed(tracker.events))
        user_events = [d for d in reversed_events if d['event'] == 'user']

        if tracker.get_slot('cc_life_subtopics_eng') == 'diet':
            dispatcher.utter_message(template='utter_transition_question_eng')
        elif tracker.get_slot('cc_comm_subtopics_eng') == 'advocacy':
            dispatcher.utter_message(template='utter_transition_question_eng')
        elif tracker.get_slot('cc_action_topics_eng') == 'education':
            dispatcher.utter_message(template='utter_how_can_help_eng')
        else:
            dispatcher.utter_message(template='utter_anything_else_eng')

        return []

class ActionSelectFollowUpFRA(Action):

    def name(self) -> Text:
        return 'action_offer_follow_ups_fra'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        last_intent = tracker.latest_message['intent'].get('name')
        print(f'last intent is {last_intent}')

        reversed_events = list(reversed(tracker.events))
        user_events = [d for d in reversed_events if d['event'] == 'user']

        if tracker.get_slot('cc_life_subtopics_fra') == 'diet_fra':
            dispatcher.utter_message(template='utter_transition_question_fra')
        elif tracker.get_slot('cc_comm_subtopics_fra') == 'advocacy_fr':
            dispatcher.utter_message(template='utter_transition_question_fra')
        elif tracker.get_slot('cc_action_topics_fra') == 'education_fr':
            dispatcher.utter_message(template='utter_how_can_help_fra')
        else:
            dispatcher.utter_message(template='utter_anything_else_fra')

        return []

class ActionSelectFollowUpSPA(Action):

    def name(self) -> Text:
        return 'action_offer_follow_ups_spa'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        last_intent = tracker.latest_message['intent'].get('name')
        print(f'last intent is {last_intent}')

        reversed_events = list(reversed(tracker.events))
        user_events = [d for d in reversed_events if d['event'] == 'user']

        sub_topic = tracker.get_slot('cc_comm_subtopics_spa')
        print(f'cc_comm_subtopics_spa value is {sub_topic}')

        if tracker.get_slot('cc_life_subtopics_spa') == 'diet_spa':
            dispatcher.utter_message(template='utter_transition_question_spa')
        elif tracker.get_slot('cc_comm_subtopics_spa') == 'advocacy_spa':
            dispatcher.utter_message(template='utter_transition_question_spa')
        elif tracker.get_slot('cc_action_topics_spa') == 'education_spa':
            dispatcher.utter_message(template='utter_how_can_help_spa')
        else:
            dispatcher.utter_message(template='utter_anything_else_spa')

        return []


class ActionSelectFollowUpARA(Action):

    def name(self) -> Text:
        return 'action_offer_follow_ups_ara'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        last_intent = tracker.latest_message['intent'].get('name')
        print(f'last intent is {last_intent}')

        reversed_events = list(reversed(tracker.events))
        user_events = [d for d in reversed_events if d['event'] == 'user']

        if tracker.get_slot('cc_life_subtopics_ara') == 'diet_ara':
            dispatcher.utter_message(template='utter_transition_question_ara')
        elif tracker.get_slot('cc_comm_subtopics_ara') == 'advocacy_ara':
            dispatcher.utter_message(template='utter_transition_question_ara')
        elif tracker.get_slot('cc_action_topics_ara') == 'education_ara':
            dispatcher.utter_message(template='utter_how_can_help_ara')
        else:
            dispatcher.utter_message(template='utter_anything_else_ara')

        return []


class ActionTellMeMoreENG(Action):

    '''
    This (one for each language) handles the response to the follow ups.
    Utters the follow up response template, and an anything_else
    '''

    def name(self) -> Text:
        return 'action_deal_with_follow_ups_eng'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_slot('cc_life_subtopics_eng') == 'diet':
            dispatcher.utter_message(template='utter_answer_ccc_lifestyle_local_diet_eng')
            dispatcher.utter_message(template='utter_anything_else_eng')
        elif tracker.get_slot('cc_comm_subtopics_eng') == 'advocacy':
            dispatcher.utter_message(template='utter_answer_ccc_advocacy_toolkit_eng')
            dispatcher.utter_message(template='utter_anything_else_eng')
        # else:
        #     dispatcher.utter_message(template='utter_anything_else_eng')

        return []

class ActionTellMeMoreFRA(Action):

    def name(self) -> Text:
        return 'action_deal_with_follow_ups_fra'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_slot('cc_life_subtopics_fra') == 'diet_fra':
            dispatcher.utter_message(template='utter_answer_ccc_lifestyle_local_diet_fra')
            dispatcher.utter_message(template='utter_anything_else_fra')
        elif tracker.get_slot('cc_comm_subtopics_fra') == 'advocacy_fra':
            dispatcher.utter_message(template='utter_answer_ccc_advocacy_toolkit_fra')
            dispatcher.utter_message(template='utter_anything_else_fra')
        # else:
        #     dispatcher.utter_message(template='utter_anything_else_fra')

        return []


class ActionTellMeMoreSPA(Action):

    def name(self) -> Text:
        return 'action_deal_with_follow_ups_spa'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_slot('cc_life_subtopics_spa') == 'diet_spa':
            dispatcher.utter_message(template='utter_answer_ccc_lifestyle_local_diet_spa')
            dispatcher.utter_message(template='utter_anything_else_spa')
        elif tracker.get_slot('cc_comm_subtopics_spa') == 'advocacy_spa':
            dispatcher.utter_message(template='utter_answer_ccc_advocacy_toolkit_spa')
            dispatcher.utter_message(template='utter_anything_else_spa')
        # else:
        #     dispatcher.utter_message(template='utter_anything_else_spa')

        return []

class ActionTellMeMoreARA(Action):

    def name(self) -> Text:
        return 'action_deal_with_follow_ups_ara'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_slot('cc_life_subtopics_ara') == 'diet_ara':
            dispatcher.utter_message(template='utter_answer_ccc_lifestyle_local_diet_ara')
            dispatcher.utter_message(template='utter_anything_else_ara')
        elif tracker.get_slot('cc_comm_subtopics_ara') == 'advocacy_ara':
            dispatcher.utter_message(template='utter_answer_ccc_advocacy_toolkit_ara')
            dispatcher.utter_message(template='utter_anything_else_ara')

        # else:
        #     dispatcher.utter_message(template='utter_anything_else_ara')

        return []

class ActionResetFull(Action):

    '''
    We need this to reset all the slots at various stages, especially:
    1. If the user says "hello", signalling a restarted conversation
    2. If we have said everything we have to say on a certain topic.
       This allows the user to re-run the form to ask something else.
    '''

    def name(self):
        return "action_reset_full"

    def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]
#        return []

class ActionMyFallbackENG(Action):

    '''
    This would handle low confidence intent classifications. Not currently
    being used. Might make sense if the scope of the bot grows.
    '''

    def name(self) -> Text:
        return "action_my_fallback_eng"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text='CA says: Sorry, not sure what you mean')

        return []

class RecommendCCActionFormENG(FormAction):

    '''
    An implementation of the form to recommend actions (one for each language).
    Asks a general topic area, then offers sub-topics.
    Worth considering reimplementing using intents directly
    from the button payloads.
    We are currently using from_text so that we can also capture the input
    as a single word outside this context.
    '''

    def name(self) -> Text:
        return "form_recommend_cc_action_eng"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        if tracker.get_slot('cc_action_topics_eng') == 'lifestyle':
            return['cc_action_topics_eng','cc_life_subtopics_eng']
        if tracker.get_slot('cc_comm_subtopics_eng') == 'group_activities':
            return["cc_action_topics_eng",'cc_comm_subtopics_eng','cc_group_action_eng']
        if tracker.get_slot('cc_action_topics_eng') == 'education':
            return["cc_action_topics_eng"]
        else:
            return['cc_action_topics_eng','cc_comm_subtopics_eng']

    def slot_mappings(self) -> Text:
        return {
        # might be worth considering filling these with from _intent directly.
        'cc_action_topics_eng':     [ self.from_text(),
                                      self.from_entity(entity='cc_action_topics_eng')
                                    ],
        'cc_comm_subtopics_eng':    self.from_text(),
        'cc_group_action_eng':      self.from_text(),
        'cc_life_subtopics_eng':    self.from_text(),

        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        # Lifestyle options
        if tracker.get_slot('cc_life_subtopics_eng') == 'shopping':
            dispatcher.utter_message(template='utter_answer_ccc_plastic_bags_eng')
#            dispatcher.utter_message(text='CA says: Don\'t use plastic bags.')
        if tracker.get_slot('cc_life_subtopics_eng') == 'diet':
            dispatcher.utter_message(template='utter_answer_ccc_lifestyle_diet_eng')
#            dispatcher.utter_message(text='CA says: You are what you eat.')
        if tracker.get_slot('cc_life_subtopics_eng') == 'travel':
            dispatcher.utter_message(template='utter_answer_ccc_lifestyle_transportation_eng')
#            dispatcher.utter_message(text='CA says: Travel broadens the mind, and destroys the planet.')
        # Community options
        if tracker.get_slot('cc_comm_subtopics_eng') == 'prevention':
            dispatcher.utter_message(template='utter_answer_ccc_prevention_plans_eng')
#            dispatcher.utter_message(text='CA says: Prevention is better than cure')
        if tracker.get_slot('cc_comm_subtopics_eng') == 'advocacy':
            dispatcher.utter_message(template='utter_answer_ccc_advocacy_intro_eng')
#            dispatcher.utter_message(template='utter_answer_ccc_advocacy_toolkit_eng')
#            dispatcher.utter_message(text='CA says: When the world is silent, even one voice becomes powerful.')
        # Community actitivies...
        if tracker.get_slot('cc_group_action_eng') == 'planting_trees':
            dispatcher.utter_message(template="utter_answer_ccc_group_planting_trees_eng")
        if tracker.get_slot('cc_group_action_eng') == 'shared_gardens':
            dispatcher.utter_message(template='utter_answer_ccc_shared_gardens_eng')
        if tracker.get_slot('cc_group_action_eng') == 'games':
            dispatcher.utter_message(template='utter_answer_ccc_games_eng')
        if tracker.get_slot('cc_action_topics_eng') == 'education':
            dispatcher.utter_message(template='utter_start_cc_education_eng')
        else:
#            dispatcher.utter_message(template="utter_greet")
            dispatcher.utter_message(template='That\'s great!')

        return[]

class RecommendCCActionFormFRA(FormAction):

    def name(self) -> Text:
        return "form_recommend_cc_action_fra"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        if tracker.get_slot('cc_action_topics_fra') == 'lifestyle_fra':
            return['cc_action_topics_fra','cc_life_subtopics_fra']
        if tracker.get_slot('cc_comm_subtopics_fra') == 'group_activities_fra':
            return["cc_action_topics_fra",'cc_comm_subtopics_fra','cc_group_action_fra']
        if tracker.get_slot('cc_action_topics_fra') == 'education_fra':
            return["cc_action_topics_fra"]
        else:
            return['cc_action_topics_fra','cc_comm_subtopics_fra']

    def slot_mappings(self) -> Text:
        return {
        'cc_action_topics_fra':     [ self.from_text(),
                                      #self.from_intent(entity='cc_action_topics_fra')
                                    ],
        'cc_comm_subtopics_fra':    self.from_text(),
        'cc_group_action_fra':      self.from_text(),
        'cc_life_subtopics_fra':    self.from_text(),

        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        # Lifestyle options
        if tracker.get_slot('cc_life_subtopics_fra') == 'shopping_fra':
            dispatcher.utter_message(template='utter_answer_ccc_plastic_bags_fra')
#            dispatcher.utter_message(text='CA says: Don\'t use plastic bags.')
        if tracker.get_slot('cc_life_subtopics_fra') == 'diet_fra':
            dispatcher.utter_message(template='utter_answer_ccc_lifestyle_diet_fra')
#            dispatcher.utter_message(text='CA says: You are what you eat.')
        if tracker.get_slot('cc_life_subtopics_fra') == 'travel_fra':
            dispatcher.utter_message(template='utter_answer_ccc_lifestyle_transportation_fra')
#            dispatcher.utter_message(text='CA says: Travel broadens the mind, and destroys the planet.')
        # Community options
        if tracker.get_slot('cc_comm_subtopics_fra') == 'prevention_fra':
            dispatcher.utter_message(template='utter_answer_ccc_prevention_plans_fra')
#            dispatcher.utter_message(text='CA says: Prevention is better than cure')
        if tracker.get_slot('cc_comm_subtopics_fra') == 'advocacy_fra':
            dispatcher.utter_message(template='utter_answer_ccc_advocacy_intro_fra')
#            dispatcher.utter_message(text='CA says: When the world is silent, even one voice becomes powerful.')
        # Community actitivies...
        if tracker.get_slot('cc_group_action_fra') == 'planting_trees_fra':
            dispatcher.utter_message(template="utter_answer_ccc_group_planting_trees_fra")
        if tracker.get_slot('cc_group_action_fra') == 'shared_gardens_fra':
            dispatcher.utter_message(template='utter_answer_ccc_shared_gardens_fra')
        if tracker.get_slot('cc_group_action_fra') == 'games_fra':
            dispatcher.utter_message(template='utter_answer_ccc_games_fra')
        if tracker.get_slot('cc_action_topics_fra') == 'education_fra':
            dispatcher.utter_message(template='utter_start_cc_education_fra')
        else:
#            dispatcher.utter_message(template="utter_greet")
            dispatcher.utter_message(template='That\'s great!')
        return[]

class RecommendCCActionFormSPA(FormAction):

    def name(self) -> Text:
        return "form_recommend_cc_action_spa"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        if tracker.get_slot('cc_action_topics_spa') == 'lifestyle_spa':
            return['cc_action_topics_spa','cc_life_subtopics_spa']
        if tracker.get_slot('cc_comm_subtopics_spa') == 'group_activities_spa':
            return["cc_action_topics_spa",'cc_comm_subtopics_spa','cc_group_action_spa']
        if tracker.get_slot('cc_action_topics_spa') == 'education_spa':
            return["cc_action_topics_spa"]
        else:
            return['cc_action_topics_spa','cc_comm_subtopics_spa']

    def slot_mappings(self) -> Text:
        return {
        'cc_action_topics_spa':     self.from_text(),
        'cc_comm_subtopics_spa':    self.from_text(),
        'cc_group_action_spa':      self.from_text(),
        'cc_life_subtopics_spa':    self.from_text(),

        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        # Lifestyle options
        if tracker.get_slot('cc_life_subtopics_spa') == 'shopping_spa':
            dispatcher.utter_message(template='utter_answer_ccc_plastic_bags_spa')
#            dispatcher.utter_message(text='CA says: Don\'t use plastic bags.')
        if tracker.get_slot('cc_life_subtopics_spa') == 'diet_spa':
            dispatcher.utter_message(template='utter_answer_ccc_lifestyle_diet_spa')
#            dispatcher.utter_message(text='CA says: You are what you eat.')
        if tracker.get_slot('cc_life_subtopics_spa') == 'travel_spa':
            dispatcher.utter_message(template='utter_answer_ccc_lifestyle_transportation_spa')
#            dispatcher.utter_message(text='CA says: Travel broadens the mind, and destroys the planet.')
        # Community options
        if tracker.get_slot('cc_comm_subtopics_spa') == 'prevention_spa':
            dispatcher.utter_message(template='utter_answer_ccc_prevention_plans_spa')
#            dispatcher.utter_message(text='CA says: Prevention is better than cure')
        if tracker.get_slot('cc_comm_subtopics_spa') == 'advocacy_spa':
            dispatcher.utter_message(template='utter_answer_ccc_advocacy_intro_spa')
#            dispatcher.utter_message(text='CA says: When the world is silent, even one voice becomes powerful.')
        # Community actitivies...
        if tracker.get_slot('cc_group_action_spa') == 'planting_trees_spa':
            dispatcher.utter_message(template="utter_answer_ccc_group_planting_trees_spa")
        if tracker.get_slot('cc_group_action_spa') == 'shared_gardens_spa':
            dispatcher.utter_message(template='utter_answer_ccc_shared_gardens_spa')
        if tracker.get_slot('cc_group_action_spa') == 'games_spa':
            dispatcher.utter_message(template='utter_answer_ccc_games_spa')
        if tracker.get_slot('cc_action_topics_spa') == 'education_spa':
            dispatcher.utter_message(template='utter_start_cc_education_spa')
        else:
#            dispatcher.utter_message(template="utter_greet")
            dispatcher.utter_message(template='That\'s great!')
        return[]


class RecommendCCActionFormARA(FormAction):

    def name(self) -> Text:
        return "form_recommend_cc_action_ara"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        if tracker.get_slot('cc_action_topics_ara') == 'lifestyle_ara':
            return['cc_action_topics_ara','cc_life_subtopics_ara']
        if tracker.get_slot('cc_comm_subtopics_ara') == 'group_activities_ara':
            return["cc_action_topics_ara",'cc_comm_subtopics_ara','cc_group_action_ara']
        if tracker.get_slot('cc_action_topics_ara') == 'education_ara':
            return["cc_action_topics_ara"]
        else:
            return['cc_action_topics_ara','cc_comm_subtopics_ara']

    def slot_mappings(self) -> Text:
        return {
        'cc_action_topics_ara':     self.from_text(),
        'cc_comm_subtopics_ara':    self.from_text(),
        'cc_group_action_ara':      self.from_text(),
        'cc_life_subtopics_ara':    self.from_text(),

        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        # Lifestyle options
        if tracker.get_slot('cc_life_subtopics_ara') == 'shopping_ara':
            dispatcher.utter_message(template='utter_answer_ccc_plastic_bags_ara')
#            dispatcher.utter_message(text='CA says: Don\'t use plastic bags.')
        if tracker.get_slot('cc_life_subtopics_ara') == 'diet_ara':
            dispatcher.utter_message(template='utter_answer_ccc_lifestyle_diet_ara')
#            dispatcher.utter_message(text='CA says: You are what you eat.')
        if tracker.get_slot('cc_life_subtopics_ara') == 'travel_ara':
            dispatcher.utter_message(template='utter_answer_ccc_lifestyle_transportation_ara')
#            dispatcher.utter_message(text='CA says: Travel broadens the mind, and destroys the planet.')
        # Community options
        if tracker.get_slot('cc_comm_subtopics_ara') == 'prevention_ara':
            dispatcher.utter_message(template='utter_answer_ccc_prevention_plans_ara')
#            dispatcher.utter_message(text='CA says: Prevention is better than cure')
        if tracker.get_slot('cc_comm_subtopics_ara') == 'advocacy_ara':
            dispatcher.utter_message(template='utter_answer_ccc_advocacy_intro_ara')
#            dispatcher.utter_message(text='CA says: When the world is silent, even one voice becomes powerful.')
        # Community actitivies...
        if tracker.get_slot('cc_group_action_ara') == 'planting_trees_ara':
            dispatcher.utter_message(template="utter_answer_ccc_group_planting_trees_ara")
        if tracker.get_slot('cc_group_action_ara') == 'shared_gardens_ara':
            dispatcher.utter_message(template='utter_answer_ccc_shared_gardens_ara')
        if tracker.get_slot('cc_group_action_ara') == 'games_ara':
            dispatcher.utter_message(template='utter_answer_ccc_games_ara')
        if tracker.get_slot('cc_action_topics_ara') == 'education_ara':
            dispatcher.utter_message(template='utter_start_cc_education_ara')
        else:
#            dispatcher.utter_message(template="utter_greet")
            dispatcher.utter_message(template='That\'s great!')
        return[]


class FirstTimeFormENG(FormAction):

    '''
    This is not deployed currently in the climate change bot.
    '''

    def name(self) -> Text:
        return "form_first_time_eng"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        if tracker.get_slot("first_time_eng") == True:
            return["first_time_eng","given_name_eng","location_eng"]
        else:
            return["first_time_eng"]

    def slot_mappings(self) -> Text:
        return {
        "first_time_eng": [
            self.from_intent(intent="affirm_eng", value=True),
            self.from_intent(intent="deny_eng", value=False)
            ],
        "given_name_eng": self.from_text(),
        "location_eng": self.from_text()
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        if tracker.get_slot("first_time_eng") == False:
            dispatcher.utter_message(template="utter_welcome_back_eng")
        else:
#            dispatcher.utter_message(template="utter_greet")
            dispatcher.utter_message(template="utter_greet_with_name_eng")
        return[]


class FirstTimeFormFRA(FormAction):

    def name(self) -> Text:
        return "form_first_time_fra"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        if tracker.get_slot("first_time_fra") == True:
            return["first_time_fra","given_name_fra","location_fra"]
        else:
            return["first_time_fra"]

    def slot_mappings(self) -> Text:
        return {
        "first_time_fra": [
            self.from_intent(intent="affirm_fra", value=True),
            self.from_intent(intent="deny_fra", value=False)
            ],
        "given_name_fra": self.from_text(),
        "location_fra": self.from_text()
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        if tracker.get_slot("first_time_fra") == False:
            dispatcher.utter_message(template="utter_welcome_back_fra")
        else:
#            dispatcher.utter_message(template="utter_greet")
            dispatcher.utter_message(template="utter_greet_with_name_fra")
        return[]

class FirstTimeFormSPA(FormAction):

    def name(self) -> Text:
        return "form_first_time_spa"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        if tracker.get_slot("first_time_spa") == True:
            return["first_time_spa","given_name_spa","location_spa"]
        else:
            return["first_time_spa"]

    def slot_mappings(self) -> Text:
        return {
        "first_time_spa": [
            self.from_intent(intent="affirm_spa", value=True),
            self.from_intent(intent="deny_spa", value=False)
            ],
        "given_name_spa": self.from_text(),
        "location_spa": self.from_text()
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        if tracker.get_slot("first_time_spa") == False:
            dispatcher.utter_message(template="utter_welcome_back_spa")
        else:
#            dispatcher.utter_message(template="utter_greet")
            dispatcher.utter_message(template="utter_greet_with_name_spa")
        return[]

class FirstTimeFormARA(FormAction):

    def name(self) -> Text:
        return "form_first_time_ara"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        if tracker.get_slot("first_time_ara") == True:
            return["first_time_ara","given_name_ara","location_ara"]
        else:
            return["first_time_ara"]

    def slot_mappings(self) -> Text:
        return {
        "first_time_ara": [
            self.from_intent(intent="affirm_ara", value=True),
            self.from_intent(intent="deny_ara", value=False)
            ],
        "given_name_ara": self.from_text(),
        "location_ara": self.from_text()
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        if tracker.get_slot("first_time_ara") == False:
            dispatcher.utter_message(template="utter_welcome_back_ara")
        else:
#            dispatcher.utter_message(template="utter_greet")
            dispatcher.utter_message(template="utter_greet_with_name_ara")
        return[]

class FeedbackFormENG(FormAction):

    '''
    This is not currently implemented in the climate change bot.
    '''

    def name(self) -> Text:
        return "form_feedback_eng"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        # if the answer to "Did we do OK?" is no...
        if tracker.get_slot("feedback_eng") == False:
            return["feedback_eng", "feedback_reason_eng"]
        else:
            return["feedback_eng"]

    def slot_mappings(self) -> Text:
        return {
        "feedback_eng": [
            self.from_intent(intent="affirm_eng", value=True),
            self.from_intent(intent="deny_eng", value=False)
            ],
        "feedback_reason_eng": self.from_text()
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        dispatcher.utter_message(template="utter_thanks_for_your_feedback_eng")
        return[]

class FeedbackFormFRA(FormAction):

    def name(self) -> Text:
        return "form_feedback_fra"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        # if the answer to "Did we do OK?" is no...
        if tracker.get_slot("feedback_fra") == False:
            return["feedback_fr", "feedback_reason_fr"]
        else:
            return["feedback_fra"]

    def slot_mappings(self) -> Text:
        return {
        "feedback_fra": [
            self.from_intent(intent="affirm_fra", value=True),
            self.from_intent(intent="deny_fra", value=False)
            ],
        "feedback_reason_fra": self.from_text()
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        dispatcher.utter_message(template="utter_thanks_for_your_feedback_fra")
        return[]

class FeedbackFormSPA(FormAction):

    def name(self) -> Text:
        return "form_feedback_spa"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        # if the answer to "Did we do OK?" is no...
        if tracker.get_slot("feedback_spa") == False:
            return["feedback_spa", "feedback_reason_spa"]
        else:
            return["feedback_spa"]

    def slot_mappings(self) -> Text:
        return {
        "feedback_spa": [
            self.from_intent(intent="affirm_spa", value=True),
            self.from_intent(intent="deny_spa", value=False)
            ],
        "feedback_reason_spa": self.from_text()
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        dispatcher.utter_message(template="utter_thanks_for_your_feedback_spa")
        return[]

class FeedbackFormARA(FormAction):

    def name(self) -> Text:
        return "form_feedback_ara"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        # if the answer to "Did we do OK?" is no...
        if tracker.get_slot("feedback_ara") == False:
            return["feedback_ara", "feedback_reason_ln"]
        else:
            return["feedback_ara"]

    def slot_mappings(self) -> Text:
        return {
        "feedback_ara": [
            self.from_intent(intent="affirm_ara", value=True),
            self.from_intent(intent="deny_ara", value=False)
            ],
        "feedback_reason_ara": self.from_text()
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        dispatcher.utter_message(template="utter_thanks_for_your_feedback_ara")
        return[]

class LanguageQuestionsFormENG(FormAction):

    '''
    This is not currently implemented in the climate change bot.
    '''

    def name(self) -> Text:
        return "form_language_questions_eng"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        return["language_at_home_eng"]

    def slot_mappings(self) -> Text:
        return {
        "language_at_home_eng": self.from_text()
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        dispatcher.utter_message(template="utter_get_back_on_topic_eng")
        return[]

class LanguageQuestionsFormFRA(FormAction):

    def name(self) -> Text:
        return "form_language_questions_fra"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        return["language_at_home_fra"]

    def slot_mappings(self) -> Text:
        return {
        "language_at_home_fra": self.from_text()
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        dispatcher.utter_message(template="utter_get_back_on_topic_fra")
        return[]

class LanguageQuestionsFormSPA(FormAction):

    def name(self) -> Text:
        return "form_language_questions_spa"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        return["language_at_home_spa"]

    def slot_mappings(self) -> Text:
        return {
        "language_at_home_spa": self.from_text()
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        dispatcher.utter_message(template="utter_get_back_on_topic_spa")
        return[]

class LanguageQuestionsFormARA(FormAction):

    def name(self) -> Text:
        return "form_language_questions_ara"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        return["language_at_home_ara"]

    def slot_mappings(self) -> Text:
        return {
        "language_at_home_ara": self.from_text()
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        dispatcher.utter_message(template="utter_get_back_on_topic_ara")
        return[]

class MythSourceFormENG(FormAction):

    '''
    This is not currently implemented in the climate change bot.
    '''

    def name(self) -> Text:
        return "form_myth_source_eng"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        return["myth_source_eng"]

    def slot_mappings(self) -> Text:
        return {
        "myth_source_eng": self.from_text()
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        dispatcher.utter_message(template="utter_thanks_for_your_feedback_eng")
        return[]

class MythSourceFormFRA(FormAction):

    def name(self) -> Text:
        return "form_myth_source_fra"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        return["myth_source_fra"]

    def slot_mappings(self) -> Text:
        return {
        "myth_source_fra": self.from_text()
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        dispatcher.utter_message(template="utter_thanks_for_your_feedback_fra")
        return[]

class MythSourceFormSPA(FormAction):

    def name(self) -> Text:
        return "form_myth_source_spa"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        return["myth_source_spa"]

    def slot_mappings(self) -> Text:
        return {
        "myth_source_spa": self.from_text()
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        dispatcher.utter_message(template="utter_thanks_for_your_feedback_spa")
        return[]

class MythSourceFormARA(FormAction):

    def name(self) -> Text:
        return "form_myth_source_ara"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        return["myth_source_ara"]

    def slot_mappings(self) -> Text:
        return {
        "myth_source_ara": self.from_text()
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        dispatcher.utter_message(template="utter_thanks_for_your_feedback_ara")
        return[]

class ActionGetInfectionStatsENG(Action):

    '''
    This is not currently implemented in the climate change bot.
    '''

    def name(self) -> Text:
        return "action_get_infection_stats_eng"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # this is where to paste the call to API
        country = "DRC"
        url = "https://covid-193.p.rapidapi.com/statistics"
        headers = { 'x-rapidapi-host': "covid-193.p.rapidapi.com", 'x-rapidapi-key': "c41cd0c62dmshb99d2fb0a63207dp1775a0jsna4f33aea1040"}
        query_string = {"country":country}

        # get the response
        response = requests.request("GET", url, headers=headers, params=query_string)
        response_JSON = response.json()

        #get the bits of the response we want
        active = response_JSON['response'][0]['cases']['active']
        new = response_JSON['response'][0]['cases']['new']
        recovered = response_JSON['response'][0]['cases']['recovered']
        new_deaths = response_JSON['response'][0]['deaths']['new']
        total_deaths = response_JSON['response'][0]['deaths']['total']

        if not new_deaths:
            new_deaths = 0
        if not new:
            new = 0

        dispatcher.utter_message(template="utter_get_infection_stats_eng",
                                 active = active,
                                 new = new,
                                 recovered = recovered,
                                 country = country,
                                 new_deaths = new_deaths,
                                 total_deaths = total_deaths
                                 )

        return []

class ActionGetInfectionStatsFRA(Action):

    def name(self) -> Text:
        return "action_get_infection_stats_fra"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # this is where to paste the call to API
        country = "DRC"
        url = "https://covid-193.p.rapidapi.com/statistics"
        headers = { 'x-rapidapi-host': "covid-193.p.rapidapi.com", 'x-rapidapi-key': "c41cd0c62dmshb99d2fb0a63207dp1775a0jsna4f33aea1040"}
        query_string = {"country":country}

        # get the response
        response = requests.request("GET", url, headers=headers, params=query_string)
        response_JSON = response.json()

        #get the bits of the response we want
        active = response_JSON['response'][0]['cases']['active']
        new = response_JSON['response'][0]['cases']['new']
        recovered = response_JSON['response'][0]['cases']['recovered']
        new_deaths = response_JSON['response'][0]['deaths']['new']
        total_deaths = response_JSON['response'][0]['deaths']['total']

        if not new_deaths:
            new_deaths = 0
        if not new:
            new = 0

        dispatcher.utter_message(template="utter_get_infection_stats_fra",
                                 active = active,
                                 new = new,
                                 recovered = recovered,
                                 country = country,
                                 new_deaths = new_deaths,
                                 total_deaths = total_deaths
                                 )

        return []

class ActionGetInfectionStatsSPA(Action):

    def name(self) -> Text:
        return "action_get_infection_stats_spa"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # this is where to paste the call to API
        country = "DRC"
        url = "https://covid-193.p.rapidapi.com/statistics"
        headers = { 'x-rapidapi-host': "covid-193.p.rapidapi.com", 'x-rapidapi-key': "c41cd0c62dmshb99d2fb0a63207dp1775a0jsna4f33aea1040"}
        query_string = {"country":country}

        # get the response
        response = requests.request("GET", url, headers=headers, params=query_string)
        response_JSON = response.json()

        #get the bits of the response we want
        active = response_JSON['response'][0]['cases']['active']
        new = response_JSON['response'][0]['cases']['new']
        recovered = response_JSON['response'][0]['cases']['recovered']
        new_deaths = response_JSON['response'][0]['deaths']['new']
        total_deaths = response_JSON['response'][0]['deaths']['total']

        if not new_deaths:
            new_deaths = 0
        if not new:
            new = 0

        dispatcher.utter_message(template="utter_get_infection_stats_spa",
                                 active = active,
                                 new = new,
                                 recovered = recovered,
                                 country = country,
                                 new_deaths = new_deaths,
                                 total_deaths = total_deaths
                                 )
#        dispatcher.utter_message(text=f'There are {active} people infected in {country}, a change of {new} on yesterday.')

        return []

class ActionGetInfectionStatsARA(Action):

    def name(self) -> Text:
        return "action_get_infection_stats_ara"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # this is where to paste the call to API
        country = "DRC"
        url = "https://covid-193.p.rapidapi.com/statistics"
        headers = { 'x-rapidapi-host': "covid-193.p.rapidapi.com", 'x-rapidapi-key': "c41cd0c62dmshb99d2fb0a63207dp1775a0jsna4f33aea1040"}
        query_string = {"country":country}

        # get the response
        response = requests.request("GET", url, headers=headers, params=query_string)
        response_JSON = response.json()

        #get the bits of the response we want
        active = response_JSON['response'][0]['cases']['active']
        new = response_JSON['response'][0]['cases']['new']
        recovered = response_JSON['response'][0]['cases']['recovered']
        new_deaths = response_JSON['response'][0]['deaths']['new']
        total_deaths = response_JSON['response'][0]['deaths']['total']

        if not new_deaths:
            new_deaths = 0
        if not new:
            new = 0

        dispatcher.utter_message(template="utter_get_infection_stats_ara",
                                 active = active,
                                 new = new,
                                 recovered = recovered,
                                 country = country,
                                 new_deaths = new_deaths,
                                 total_deaths = total_deaths
                                 )
#        dispatcher.utter_message(text=f'There are {active} people infected in {country}, a change of {new} on yesterday.')

        return []
