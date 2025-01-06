import streamlit as st
from utils import Item, warrior_profile
import random

def get_tavern_items():
    return [
        Item("Honey beer", 5, "health", -5, ":material/sports_bar:"),
        Item("Lamb shank", 15, "health", 10, ":material/stockpot:"),
        Item("Sunday roast", 30, "health", 25, ":material/stockpot:"),
    ]

tavern_items = get_tavern_items()

# Coin flip game logic
def coin_flip_game(bet_amount, bet_choice):
    # Simulate coin flip (heads or tails)
    coin = random.choice(["heads", "tails"])
    
    # Compare bet_choice with the result of the coin flip
    if bet_choice == coin:
        return True, coin  # Win, return the coin result
    else:
        return False, coin  # Lose, return the coin result

if st.session_state.warrior:
    warrior = st.session_state.warrior
   
    with st.sidebar:
        warrior_profile()

    messages = [
        f"*You push open the door to a warm and welcoming tavern where an open fire crackles in the corner. The barman greets you with a nod.*",
        f"*You push open the door to a warm and welcoming tavern where an open fire crackles in the corner. The barman greets you: Ey up {warrior.name}, how are things?*",
        f"*You push open the door to a warm and welcoming tavern where the smells of cooking meat fill the room. The barkeep seems you enterer. Ah {warrior.name}, here for the Sunday roast again?*",
        f"*You push open the door to a welcoming tavern where the locals gather around the bar and a small dog lays infront of the fire.*",
    ]
    st.markdown(random.choice(messages))

    left,right = st.columns([2, 1])
    with left:
        st.subheader("Tavern bar")
        for item in tavern_items:
            cols = st.columns([2, 1, 1])
            with cols[0]:
                st.write(f"{item.icon} {item.name} ({item.cost} gold)")
            with cols[1]:
                st.text(f"{item.effect_value} {item.effect_type}")
            with cols[2]:
                if st.button("Buy", key=f"buy_{item.name}"):
                    if warrior.gold >= item.cost:
                        warrior.gold -= item.cost
                        warrior.inventory.append(item)
                        st.toast(f"Bought {item.name}!")
                        st.session_state.combat_log.append(f"Bought {item.name}!")
                        st.rerun()
                    else:
                        st.toast(f"Not enough gold, {warrior.name}!", icon=":material/feedback:")
                        # st.session_state.combat_log.append("Not enough gold!")

        # Coin flip betting section
        st.subheader("Wager on a coin toss")

        # Add the CSS at the top of your file
        st.markdown("""
            <style>
                div[data-testid="stForm"] {
                    border: none;
                    padding: 0;
                }
            </style>
            """, unsafe_allow_html=True)

        if warrior.gold == 0:
            st.markdown(f"*You don't have any gold to bet, come back later {warrior.name}.*")
        else:
            st.markdown(f"*You have {warrior.gold} gold to bet. Choose heads or tails and place your bet. If you lose your gold goes to the tavern, if you win you double your bet.*")
            
            with st.form("betting_form"):
                col1, col2 = st.columns(2)
                with col1:
                    bet_amount = st.number_input(
                        "How much gold would you like to bet?",
                        min_value=1,
                        max_value=warrior.gold,
                        value=1,
                        step=1
                    )
                    bet_choice = st.pills("Choose heads or tails", ["heads", "tails"])
                
                submitted = st.form_submit_button("Flip Coin")
                if submitted:
                    if bet_amount > warrior.gold:
                        st.error("You don't have enough gold to place this bet.")
                    else:
                        win, coin_result = coin_flip_game(bet_amount, bet_choice)
                        
                        if win:
                            warrior.gold += bet_amount
                            st.success(f"You won! The coin landed on {coin_result}. You now have {warrior.gold} gold.")
                        else:
                            warrior.gold -= bet_amount
                            st.error(f"You lost! The coin landed on {coin_result}. You now have {warrior.gold} gold.")
                        
                        st.session_state.warrior = warrior

        st.subheader("Tavern dog")
        if st.button("Pet the dog", icon=":material/pets:"):
            dog_messages = [
                "Woof! The tavern dog wags its tail happily.",
                "The dog barks joyfully and nuzzles your hand.",
                "You pet the dog, and it rolls over for belly rubs.",
                "The tavern dog licks your hand and wags its tail furiously.",
                "The dog looks at you with big, happy eyes and lets out a contented sigh."
            ]
            st.toast(random.choice(dog_messages))

    with right:
        st.image("images/tavern_side.png", use_container_width=True)

else:
    st.error("You need to create a warrior first in order to enter the tavern.")
    st.warning("Go back to the character creation page and create your warrior.")