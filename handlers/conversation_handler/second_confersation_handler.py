from typing import Any

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters, \
    CallbackQueryHandler

from handlers.base_handler import BaseHandler

FOREST, BUNKER, OLD_HOUSE, FREEDOM, STORY, HOME = range(6)


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
                STORY: [MessageHandler(filters.Regex('^(Ні|Так)$'), cls.story)],
                HOME: [CallbackQueryHandler(cls.home)]
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
            keyboard = [
                [KeyboardButton('Ні'), KeyboardButton('Так')],
            ]

            reply_text = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            await update.message.reply_text(
                f"""
            Вам передчуття підказує що краще не заходити туди, і ви пішли на обхід дому, неймовірно але ви бачите дорогу!
            Ви виходите на дорогу а медвідь вас так і не догнав, ви ловите першу машину, водій якої виявився вашим братом який вас шукав,
            Він пояснює всю ситуацію і відвозить вас додому, і пропонує вам розказати вам що з вами сталося
            """, reply_markup=reply_text)
            return STORY
        elif answer == 'Та':
            await update.message.reply_text(
                f'Це виявився дім маніяка, ви застали його за розпиленням трупа... на цьому моменті ваша доля вирішена.')
            return ConversationHandler.END


    @staticmethod
    async def story(update: Update, context: ContextTypes.DEFAULT_TYPE):
        answer = update.message.text
        if answer == 'Так':
            keyboard = [
                [InlineKeyboardButton('Так', callback_data='Так')],
                [InlineKeyboardButton('Ні', callback_data='Ні')]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                f"""
                Річ у тім що ви ту ніч пішли пити алкоголь бо вас кинула дівчина, але раптом ви пропали, і вас не було 4 дні.
                вас шукали по всьому місту, і вас вважали мертвим.
                Прослухавши цю історію ви була вражені, проте щось ви почали відчувати що щось не так, і ви починаєте не довіряєте брату
                чи попробуєте ви втекти?
            """, reply_markup=reply_markup)
            return HOME
        elif answer == 'Ні':
            await update.message.reply_text(
                f'Брат розізлився і викинув вас з машини')
            return ConversationHandler.END

    @staticmethod
    async def home(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        data = query.data
        if data == 'Так':
            await query.edit_message_text("""
                Ви втекли з машини і ви взнали що ваш брат зрадник і він думав що ви в лісі помрете, і коли взнав що ви вижили
                хотів вас власноруч добити проте він попав в аварію під час спроби догнати вас і ви спокійно добралися додому,
                ХОРОШИЙ КІНЕЦЬ
            """)
            return ConversationHandler.END
        elif data == 'Ні':
            await query.edit_message_text("Ваш брат виявився зрадником і зарізав вас, дуже сумно але правда...")
            return ConversationHandler.END


