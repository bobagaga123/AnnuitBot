from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from utils.states import CreditInfo
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import table
from io import BytesIO
from aiogram.types import BufferedInputFile
from Callbacks.callback import MyCallback
from keyboards import cancel_kb, main_builder

router = Router()


@router.callback_query(MyCallback.filter(F.foo == "calculate"))
async def my_callback_foo(query: CallbackQuery, callback_data: MyCallback, state: FSMContext):
    await state.set_state(CreditInfo.amount)
    await query.message.answer("Введите сумму кредита:")



@router.message(Command("calculate"))
async def input_data(message: Message, state: FSMContext):
    await state.set_state(CreditInfo.amount)
    await message.answer("Введите сумму кредита:")


@router.message(CreditInfo.amount)
async def data(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(amount = message.text)
        await state.set_state(CreditInfo.percentage)
        await message.answer("Отлично, теперь напишите годовую процентную ставку (%):", reply_markup=cancel_kb)
    else:
        await message.answer("Введите число ещё раз")


@router.message(CreditInfo.percentage)
async def percent(message: Message, state: FSMContext):
    if message.text.lower() == "назад":
        await state.set_state(CreditInfo.amount)
        await message.answer("Введите сумму кредита:", reply_markup=types.ReplyKeyboardRemove())
    else:
        if message.text.replace("%", "").isdigit():
            await state.update_data(percentage=message.text.replace("%", ""))
            await state.set_state(CreditInfo.term)
            await message.answer("Отлично, теперь напишите срок кредита (мес.)")
        else:
            await message.answer("Введите число ещё раз")

@router.message(CreditInfo.term)
async def percent(message: Message, state: FSMContext):
    if message.text.lower() == "назад":
        await state.set_state(CreditInfo.percentage)
        await message.answer("Хорошо, напишите годовую процентную ставку", reply_markup=cancel_kb)
    else:
        if message.text.isdigit():
            await state.update_data(term=message.text)
            await state.set_state(CreditInfo.done_text)
            await message.answer("Произвожу рассчёт...")
            data = await state.get_data()
            result = await calc(data)

            image = await df_to_img(result)
            xlsx = await df_to_xlsx(result)

            img = BufferedInputFile(file=image, filename="result.png")
            xls = BufferedInputFile(file=xlsx, filename="result.xlsx")
            await message.answer_photo(img)

            await message.answer_document(document=xls, caption="Для удобства отправляю этот же график в формате xlsx:")
            await message.answer("Вы также можете повторно высчитать аннуитетный платеж, например, с другими данными\n\n"
                                 "Для этого воспользуйтесь командой /calculate или кнопками ниже:", reply_markup=main_builder.as_markup())

        else:
            await message.answer("Введите число ещё раз")


async def calc(data):
    Pv = float(data["amount"])
    Ry = float(data["percentage"]) / 100
    n = int(data["term"])
    r = Ry / 12
    P = (Pv * r * (1 + r) ** n) / ((1 + r) ** n - 1)
    df = pd.DataFrame(columns=['Остаток', 'Проценты', 'Основной долг', 'Сумма платежа'])
    for i in range(n):
        procent = Pv * r
        Osn = P - procent
        Pv -= Osn
        df.loc[i] = [abs(round(Pv,2)), round(procent,2), round(Osn,2), round(P,2)]
    #return string
    df.index.name = 'Номер платежа'
    df.index = df.index + 1
    return df

async def df_to_xlsx(df):
    buffer = BytesIO()
    df.to_excel(buffer)
    xls = buffer.getvalue()
    return xls

async def df_to_img(df):
    plt.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index, loc='center')
    plt.axis('off')

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0.1)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    del buffer
    return image_png