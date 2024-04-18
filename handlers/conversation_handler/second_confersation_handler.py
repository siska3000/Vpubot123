from typing import Any

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup

from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters

from handlers.base_handler import BaseHandler

FOREST, BUNKER, OLD_HOUSE, FREEDOM = range(4)


class SecondConversationHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('begining', cls.begin)],
            states={
                FOREST: [MessageHandler(filters.Regex('^(Ні|Так)$'), cls.forest)],
                BUNKER: [MessageHandler(filters.Regex('^(Ні|Так)$'), cls.bunker)],
                OLD_HOUSE: [MessageHandler(filters.Regex('^(Лишитися|Вийти)$'), cls.old_house)],
                FREEDOM: [MessageHandler(filters.Regex('^(Ні|Так)$'), cls.freedom)],
            },
            fallbacks=[CommandHandler('exit', cls.exit)]
        )

        app.add_handler(conversation_handler)

    @staticmethod
    async def begin(update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [KeyboardButton('Ні'), KeyboardButton('Так')],
        ]
        reply_text = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

        await update.message.reply_text(f"Вітаю в квесті {update.effective_user.first_name}! Чи бажаєте ви вижити?",
                                        reply_markup=reply_text)
        return FOREST

    @staticmethod
    async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f'Вихід з квесту')
        return ConversationHandler.END

    @staticmethod
    async def forest(update: Update, context: ContextTypes.DEFAULT_TYPE):
        answer = update.message.text
        if answer == 'Так':
            keyboard = [
                [KeyboardButton('Ні'), KeyboardButton('Так')],
            ]

            reply_text = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

            await update.message.reply_text(
                f"""
            Чудово! Ви прокинулися в лісі неймовірно голодні, і нічого не пам'ятаєте.
            Вам нічого не лишаєтся крім того, як ходити по лісу і шукати щось. Довго блукаючи ви находите загадковий бункер. Чи будете ви у нього заходити?
            """, reply_markup=reply_text)
            return BUNKER
        elif answer == 'Ні':
            await update.message.reply_text(f'Вихід з квесту')
            return ConversationHandler.END

    @staticmethod
    async def bunker(update: Update, context: ContextTypes.DEFAULT_TYPE):
        answer = update.message.text
        if answer == 'Так':
            keyboard = [
                [KeyboardButton('Лишитися'), KeyboardButton('Вийти')],
            ]

            reply_text = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

            await update.message.reply_text(
                f"""
            Ви заходите у підвал, і раптом на вас щось падає, це виявився скелет! На щастя він просто на вас впав ви налякалися але все гаразд,
            Ви заходите в якусь кімнату яку бачите і бачите запаси з їжою, чудово ви можете перекусити
            Ви пообідали, і у вас є вибір лишитися блукати в підвалі, чи йти на вихід і взяти з собою воду яка була разом з їжею
            """, reply_markup=reply_text)
            return OLD_HOUSE

        elif answer == 'Ні':
            await update.message.reply_text(
                f'Ви блукали по лісу нічого так і не найшли, сили покинули вас і ви померли від голоду...')
            return ConversationHandler.END

    @staticmethod
    async def old_house(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int | Any:
        answer = update.message.text
        if answer == 'Вийти':
            keyboard = [
                [KeyboardButton('Ні'), KeyboardButton('Так')],
            ]

            reply_text = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            await update.message.reply_text(
                f"""
            Ви йдете по лісу бачите здалека ведмедя! Він починає бігти на вас з великою швидкість, ви починає бігти навтьоки, біжите зі всіх сил 
            але ведмідь не відстає ви вже втрачаєте сили, і раптом ви бачите старий моторошний будинок, він може бути вашим рятівником, але щось 
            цей будинок виглядає підозріло, чи будете ви заходити у нього?
            """, reply_markup=reply_text)
            return FREEDOM

        elif answer == 'Лишитися':
            await update.message.reply_text(
                f'Почалася сильна гроза поки ви були в підвалі, і вихід завалило, ви померли від недостатку кисню')
            return ConversationHandler.END

    @staticmethod
    async def freedom(update: Update, context: ContextTypes.DEFAULT_TYPE):
        answer = update.message.text
        if answer == 'Ні':
            await update.message.reply_text(
                f"""
            Вам передчуття підказує що краще не заходити туди, і ви пішли на обхід дому, неймовірно але ви бачите дорогу!
            Ви виходите на дорогу а медвідь вас так і не догнав, ви ловите першу машину, водій якої виявився вашим братом який вас шукав,
            Він пояснює всю ситуація і відвозить вас додому, КІНЕЦЬ! 
            """)
            return ConversationHandler.END
        elif answer == 'Так':
            await update.message.reply_text(
                f'Це виявився дім маніяка, ви застали його за розпиленням трупа... на цьому моменті ваша доля вирішена.')
            return ConversationHandler.END
