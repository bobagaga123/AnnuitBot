from aiogram.fsm.state import StatesGroup, State

class CreditInfo(StatesGroup):
    amount = State()
    percentage = State()
    term = State()
    done_text = State()