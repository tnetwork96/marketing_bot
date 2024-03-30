import csv
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler
from sn.vietschool.score_crawler import ScoreCrawler


def school_info(school_name, manager):
    return {"name": school_name, "manager": manager}


sogd = "sogd"
nh = "ninhhoa"
manager_dict = {
    sogd: "TRỰC THUỘC SỞ GD&ĐT KHÁNH HOÀ",
    nh: "PHÒNG GD&ĐT Thị xã Ninh Hòa",
}
school_names_dict = {
    "nt": school_info("Nguyễn Trãi", manager_dict[sogd]),
    "tqc": school_info("Trần Quý Cáp", manager_dict[sogd]),
    "nct": school_info("Nguyễn Chí Thanh", manager_dict[sogd]),
    "tcv": school_info("Trần Cao Vân", manager_dict[sogd]),
    "dth": school_info("Đinh Tiên Hoàng", manager_dict[nh]),
    "lhp": school_info("Lê Hồng Phong", manager_dict[nh]),
    "tp": school_info("Trần Phú", manager_dict[nh]),
}


def get_help(update: Update, context: CallbackContext) -> None:
    tat_list = [f"{v['name']} -> {k}" for k, v in school_names_dict.items()]
    ten_viet_tat = '\n'.join(tat_list)
    message = ("Cú Pháp: Nhâp Tên trường - số báo danh\n"
               "Ví dụ : Muốn xem điểm của sbd 666025 trường Đinh Tiên Hoàng\n"
               "-> Gõ dth-666025\n"
               f"Tên viết tắt của các trường:\n"
               f"{ten_viet_tat}"
               )
    update.message.reply_text(message)


def get_message_of_id(documents, update):
    chat_id = str(update.message.chat.id)
    for c_id in documents:
        if chat_id == c_id:
            return update.message.text.strip().lower()


def other(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    global school_names_dict
    chat_id = str(update.message.chat.id)
    try:
        message = update.message.text.strip().lower()
    except AttributeError:
        return
    ele = message.split("-")
    if len(ele) < 2:
        update.message.reply_text(u"Sai cú pháp\n"
                                  u"Nhập /help để xem hướng dẫn")
        return
    school_name = ele[0]
    sbd = ele[1]
    school_full_name = school_names_dict[school_name]["name"]
    check_exist_school_name = school_name in school_names_dict.keys()
    if not check_exist_school_name:
        update.message.reply_text(f"Không tìm thấy tên trường {ele[0]}\n"
                                  f"Nhập /help để xem hướng dẫn")
        return
    try:
        int(sbd)
    except ValueError:
        update.message.reply_text(u"Không đúng định dạng số báo danh\n"
                                  u"Nhập /help để xem hướng dẫn")
        return
    update.message.reply_text(u"Đã nhận thông tin, vui lòng đợi 1,2 phút")
    crawler = ScoreCrawler()
    row_datas = crawler.read_score("https://vietschool.vn/home/tracuudiemtracnghiem",
                                   school_names_dict[school_name]["manager"],
                                   school_full_name, sbd)
    crawler.close()
    if not row_datas:
        update.message.reply_text(f"Không tìm thấy số báo danh {sbd} "
                                  f"của trường {school_full_name}")
        return
    columns = ['STT', 'SBD', 'Họ và tên', 'Ngày sinh', 'Mã đề', 'Tên đợt chấm', 'Điểm số', 'Số câu', 'SL đúng',
               'SL sai', 'SL vi phạm', 'SL không làm', 'Phòng thi']
    csv_file_name = f'diemtracnghiem.csv'
    # Writing to CSV file
    with open(csv_file_name, 'w') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerow(columns)
        [writer.writerow(row_data) for row_data in row_datas]
    context.bot.send_document(chat_id=chat_id, document=open(csv_file_name, 'rb'))


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("6816178543:AAEmQj2IQ4wTNAqqZ9u-xDl31iJ03rfEAEo")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    # dispatcher.add_handler(CommandHandler("set_comment", set_comment))
    dispatcher.add_handler(CommandHandler("start", get_help))
    dispatcher.add_handler(CommandHandler("help", get_help))
    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.all, other))

    # Start the Bot
    updater.start_polling()
    updater.idle()


main()
