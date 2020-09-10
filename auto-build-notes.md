# Notes on automatically building Clara
### The climate change bot

Right now we can't generate the bot code directly from the sheet, we need to make some changes by hand.
These are described here, but may be implemented later in the builder script `cc_bot_model_to_rasa-v2.2.py` - which is a direct copy of the covid builder script with just the sheets swapped out.

We should keep this file up to date as long as manual changes to the Rasa files are still needed.

1. Slots in stories

   The builder script doesn't currently support slot constraints in stories, like this:

   `slot{"cc_action_topics_eng" : "advocacy"}`

   These get mangled to `utter_slot{...}_eng` (etc.), the script needs to leave them alone.

2. Entities

   Entities are not currently supported in the model, so we are adding them by hand to the domain file. There is just one entity (per language) in the current model, but either an entity tab  should be added to allow entities to be created in the model.

   Currently adding:

   ```yaml
    entities:
     - cc_action_topics_eng
     - cc_action_topics_fra
     - cc_action_topics_spa
     - cc_action_topics_ara
   ```

3. Language independent actions

   We have two actions `action_reset_full` and `action_handle_no`, which should be left alone.

   Currently it gets copied one per language.

   **Note: this is also then broken in the the `stories.md` file.**

4. Button payloads

   We need these to be multiplied per language, but there may be a more elegant way of handling this. Right now though, the assumption that all payloads in a multilingual form are the same seems too restrictive.

   Needs more thought.

---
:tada: Andrew
