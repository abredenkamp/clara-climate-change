#### This file contains tests to evaluate that your bot behaves as expected.
#### If you want to learn more, please see the docs: https://rasa.com/docs/rasa/user-guide/testing-your-assistant/

## New Story

* greet_fra: Bonjour
  - utter_reply_greeting_fra
  - utter_get_informed_consent_fra
  - form_first_time_fra
  - form{"name":"form_first_time_fra"}
  - slot{"requested_slot":"first_time_fra"}
* affirm_fra: Oui
  - form_first_time_fra
  - slot{"first_time_fra":true}
  - slot{"requested_slot":"given_name_fra"}
* covid_myth_fruits_fra: Roger
  - form_first_time_fra
  - slot{"given_name_fra":"Roger"}
  - slot{"requested_slot":"location_fra"}
* ask_for_local_stats_lin: kivu_nord
  - form_first_time_fra
  - slot{"location_fra":"kivu_nord"}
  - form{"name":null}
  - slot{"requested_slot":null}
  - utter_set_expectations_fra
* ask_for_local_stats_fra: Combien de morts a Goma?
  - utter_no_local_stats_fra
  - action_get_infection_stats_fra
* covid_myth_garlic_fra: Est-ce que l'ail peut guérir le virus?
  - utter_answer_covid_myth_garlic_fra
  - form_myth_source_fra
  - form{"name":"form_myth_source_fra"}
  - slot{"requested_slot":"myth_source_fra"}
* out_of_scope_swc: whatsapp
  - form_myth_source_fra
  - slot{"myth_source_fra":"whatsapp"}
  - form{"name":null}
  - slot{"requested_slot":null}
  - utter_anything_else_fra
* goodbye_fra: Non, au revoir
  - form_feedback_fra
  - form{"name":"form_feedback_fra"}
  - slot{"requested_slot":"feedback_fra"}
* affirm_fra: /affirm_fra
  - form_feedback_fra
  - slot{"feedback_fra":true}
  - form{"name":null}
  - slot{"requested_slot":null}






<!-- ## greet_fr
* greet_fr: Bonjour
 - utter_reply_greeting_fr
 - utter_get_informed_consent_fr
 - form_first_time_fr
* form: inform: Oui
 - form: form_first_time_fr
* form: inform: Roger
 - form: form_first_time_fr
 - form{"name": null}
 - utter_greet_with_name_fr
 - utter_set_expectations_fr

## greet_sw
* greet_sw: Jambo
  - utter_reply_greeting_sw
  - utter_get_informed_consent_fsw
  - form_first_time_sw
* form: inform: Ndio
  - form: form_first_time_sw
* form: inform: Roger
  - form: form_first_time_sw
  - form{"name": null}
  - utter_greet_with_name_sw
  - utter_set_expectations_sw -->




<!-- ## say goodbye
* goodbye: Au revoir!
  - utter_goodbye -->


<!-- * check_earnings: How much did i earn
    - transact_search_form
    - form{"name":"transact_search_form"}
* transfer_money: i want to transfer money
    - utter_ask_switch_goal
* affirm: yes
    - transfer_form
    - form{"name":"transfer_form"}
* form: inform: to [Paul](PERSON)
    - form: transfer_form
* form: inform: [$45](amount-of-money:45)
    - form: transfer_form
* form: affirm: /affirm
    - form: transfer_form
    - form{"name":null}
    - utter_ask_back_to_transact
* deny: no
    - utter_ok


## happy path 1
* greet: hello there!
  - utter_greet
* mood_great: amazing
  - utter_happy

## happy path 2
* greet: hello there!
  - utter_greet
* mood_great: amazing
  - utter_happy
* goodbye: bye-bye!
  - utter_goodbye

## sad path 1
* greet: hello
  - utter_greet
* mood_unhappy: not good
  - utter_cheer_up
  - utter_did_that_help
* affirm: yes
  - utter_happy

## sad path 2
* greet: hello
  - utter_greet
* mood_unhappy: not good
  - utter_cheer_up
  - utter_did_that_help
* deny: not really
  - utter_goodbye

## sad path 3
* greet: hi
  - utter_greet
* mood_unhappy: very terrible
  - utter_cheer_up
  - utter_did_that_help
* deny: no
  - utter_goodbye


## bot challenge
* bot_challenge: are you a bot?
  - utter_iamabot -->
