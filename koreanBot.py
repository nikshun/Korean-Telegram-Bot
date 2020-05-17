import logging, random
import os
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ( Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from random import randint

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(token='1157461190:AAHwayswiyLGbIo-VQXQlshm_2R8g2ERPXc', use_context=True)
dispatcher = updater.dispatcher

logger = logging.getLogger(__name__)

QUESTION, ANSWER = range(2)

questions = [
    [["i", "u", "a", "o"],"a.jpg"],
    [["d", "s", "b", "a"],"b.jpg"],
    [["s", "j", "ch", "sh"],"ch.jpg"],
    [["t", "p", "b", "d"],"d.jpg"],
    [["yeu", "yeo", "eu", "eo"],"eo.jpg"],
    [["ou", "eu", "u", "o"],"eu.jpg"],
    [["k", "g", "b", "n"],"g.jpg"],
    [["sh", "j", "h", "ch"],"h.jpg"],
    [["u", "eu", "i", "a"],"i.jpg"],
    [["un", "in", "o", "h"],"in.jpg"],
    [["s", "ch", "sh", "j"],"j.jpg"],
    [["t", "k", "n", "g"],"k.jpg"],
    [["p", "m", "d", "b"],"m.jpg"],
    [["g", "b", "k", "n"],"n.jpg"],
    [["eo", "o", "eu", "u"],"o.jpg"],
    [["in", "m", "b", "p"],"p.jpg"],
    [["m", "s", "b", "r"],"r.jpg"],
    [["h", "ch", "j", "s"],"s.jpg"],
    [["k", "b", "d", "t"],"t.jpg"],
    [["uh", "o", "t", "u"],"u.jpg"],
    [["yeo", "yo", "yu", "ya"],"ya.jpg"],
    [["yeo", "yo", "yu", "ya"],"yeo.jpg"],
    [["yeo", "yo", "yu", "ya"],"yo.jpg"],
    [["yeo", "yo", "yu", "ya"],"yu.jpg"]
]

questionsOrder = list(range(len(questions)))


def start(update, context):
    random.shuffle(questionsOrder)
    global counter
    counter = 0
    reply_keyboard = [str(counter)]
    update.message.reply_text(str(len(questionsOrder)) + ' questions', reply_markup=ReplyKeyboardMarkup(reply_keyboard))
    # update.message.reply_text(os.path.abspath(__file__))
    return QUESTION

def question(update, context):
    global counter
    temporaryAnswers = questions[questionsOrder[counter]][0]
    random.shuffle(temporaryAnswers)
    reply_keyboard = [[temporaryAnswers[0], temporaryAnswers[1]],[temporaryAnswers[2], temporaryAnswers[3]]]
    fileName = "img/symbols/" + str(questions[questionsOrder[counter]][1])
    context.bot.send_photo(chat_id = update.effective_user.id, photo = open(fileName, 'rb'),  reply_markup=ReplyKeyboardMarkup(reply_keyboard))
    return ANSWER

def answer(update, context):
    global counter
    reply = update.message.text
    reply_keyboard = [str(counter+1)]
    answer = questions[questionsOrder[counter]][1][0:-4]
    if reply == answer:
        update.message.reply_text('Correct', reply_markup=ReplyKeyboardMarkup(reply_keyboard))
    else:
        update.message.reply_text('Answer: ' + answer, reply_markup=ReplyKeyboardMarkup(reply_keyboard))
    counter += 1
    if counter == len(questions):
        reply_keyboard = [["/start"],[]]
        update.message.reply_text('You have 0 right asnwers', reply_markup=ReplyKeyboardMarkup(reply_keyboard))
        return ConversationHandler.END
    else:
        return QUESTION




def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can play again some day.',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            QUESTION: [MessageHandler(Filters.text, question)],
            ANSWER: [MessageHandler(Filters.text, answer)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    dispatcher.add_handler(conv_handler)
    dispatcher.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()