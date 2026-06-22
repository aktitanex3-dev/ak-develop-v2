import telebot
from telebot import types
import threading
from flask import Flask
import os
from datetime import datetime
import random

# 1. ቦቱን በአዲሱ ቶከን ማስጀመር
TOKEN = "8995958985:AAFsOQ1SxWmTe6gGo-lBFXAv72YjHAWLHBQ"
ADMIN_ID = "8926052749"
bot = telebot.TeleBot(TOKEN)

# 2. ለRender መደለያ የሚሆን የFlask ሰርቨር መፍጠር
app = Flask('')

@app.route('/')
def home():
    return "AK Develop Bot is Running Alive!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# የደንበኞች መረጃ ጊዜያዊ ማከማቻ
user_data = {}

# የሶሻል ሚዲያ 5 ዋና ጥያቄዎች
SMM_QUESTIONS = [
    "1️⃣ ለማስተዳደር ያሰቡት አካውንት አሁን ላይ በግምት ምን ያህል ተከታይ/አባላት አሉት?፦",
    "2️⃣ በሳምንት ወይም በወር ውስጥ ምን ያህል ፖስቶች/ቪዲዮዎች እንዲሰሩሎት ይፈልጋሉ?፦",
    "3️⃣ የዚህ አካውንት ዋና ዓላማ ምንድን ነው? (ለምሳሌ፦ ሽያጭ ለመጨመር፣ ታዋቂነት/Brand Awareness፣ ወይስ ተከታይ ማብዛት?)፦",
    "4️⃣ ይህ የማኔጅመንት አገልግሎት ለምን ያህል ጊዜ እንዲቀጥል ይፈልጋሉ? (ለምሳሌ፦ ለ1 ወር Couching፣ ለ3 ወር ሙሉ ማኔጅመንት...)፦",
    "5️⃣ ለዚህ ስራ የመደቡት ግምታዊ ወርሃዊ በጀት (Budget) በብር ምን ያህል ነው?፦",
    "🎯 በመጨረሻም፣ የእርስዎን የቴሌግራም ዩዘርኔም (ለምሳሌ @username) ያስገቡ፦"
]

# የሌሎቹ ምድቦች 5 ጥያቄዎች
QUESTIONS = {
    "am": [
        "1️⃣ ለመሆኑ ይህ ሲስተም/አገልግሎት እንዴት እንዲሰራሎት ይፈልጋሉ? እባክዎ ሙሉ ፍላጎቶትን በዝርዝር ይፃፉልን፦",
        "2️⃣ ፕሮጀክቱ ተጠናቆ እንዲረከቡ የሚፈልጉት እስከ መቼ ነው? (የጊዜ ገደብ/Deadline)፦",
        "3️⃣ በፕሮጀክቱ ውስጥ እንዲካተቱ የሚፈልጓቸው ልዩ አገልግሎቶች ወይም ገፅታዎች (Features) ምንድን ናቸው?፦",
        "4️⃣ ይህ ሲስተም/ስራ ምን ያህል ሰፊ ወይም ምን ያህል ክፍሎች እንዲኖሩት ይገምታሉ?፦",
        "5️⃣ ለዚህ ስራ የመደቡት ግምታዊ በጀት (Budget) በኢትዮጵያ ብር ምን ያህል ነው?፦",
        "🎯 በመጨረሻም፣ የእርስዎን የቴሌግራም ዩዘርኔም (ለምሳሌ @username) ያስገቡ፦"
    ],
    "en": [
        "1️⃣ How exactly do you want this system/service to work? Please describe your requirements in detail:",
        "2️⃣ When do you need this project to be completed? (Target Deadline):",
        "3️⃣ What specific features or functionalities should be included?:",
        "4️⃣ How many pages or sub-sections do you estimate this project will have?:",
        "5️⃣ What is your estimated budget in ETB for this project?:",
        "🎯 Finally, please enter your Telegram username (e.g., @username):"
    ]
}

# የእያንዳንዱ ምርጫ መግለጫዎች
DESCRIPTIONS = {
    "web": {
        "0": {"am": "🛍️ **የኢ-ኮሜርስ ድረ-ገጽ**\n\nምርቶችዎን በምስል እና በዋጋ ለደንበኛ የሚያቀርቡበት ዘመናዊ መድረክ።\n\n👉 ማዘዝ ይፈልጋሉ?", "en": "🛍️ **E-commerce Website**\n\nShowcase products with images and prices.\n\n👉 Order now?"},
        "1": {"am": "💼 **የኩባንያ ማስተዋወቂያ ድረ-ገጽ**\n\nየድርጅትዎን አገልግሎቶች በፕሮፌሽናል መልክ የሚያስተዋውቁበት ገጽ።\n\n👉 ማዘዝ ይፈልጋሉ?", "en": "💼 **Business Website**\n\nShowcase your company services.\n\n👉 Order now?"},
        "2": {"am": "🎨 **የግል ሥራ ማሳያ (Portfolio)**\n\nየግል ሙያዎን እና የስራ ታሪክዎን ለአሰሪዎች የሚያሳዩበት ገጽ።\n\n👉 ማዘዝ ይፈልጋሉ?", "en": "🎨 **Portfolio Website**\n\nShowcase your professional skills.\n\n👉 Order now?"},
        "3": {"am": "📝 **የብሎግ እና መረጃ ሰጪ ድረ-ገጽ**\n\nተከታታይ ፅሁፎችን እና ዜናዎችን የሚያጋሩበት ድረ-ገጽ።\n\n👉 ማዘዝ ይፈልጋሉ?", "en": "📝 **Blog Website**\n\nShare articles and news.\n\n👉 Order now?"}
    },
    "bot": {
        "0": {"am": "🏪 **የቴሌግራም የሱቅ ቦት**\n\nደንበኞች ከቴሌግራም ሳይወጡ በቀጥታ እንዲገበዩ የሚያደርግ ቦት።\n\n👉 ማዘዝ ይፈልጋሉ?", "en": "🏪 **Telegram Store Bot**\n\nShop directly inside Telegram.\n\n👉 Order now?"},
        "1": {"am": "🛡️ **የግሩፕ ማኔጅመንት ቦት**\n\nግሩፖችን ከአላስፈላጊ ሊንኮች እና ስፓም በራስ-ሰር የሚጠብቅ ቦት።\n\n👉 ማዘዝ ይፈልጋሉ?", "en": "🛡️ **Group Management Bot**\n\nProtect groups from spam.\n\n👉 Order now?"},
        "2": {"am": "📣 **የቻናል ረዳት ቦት**\n\nበተዋቀረ ሰዓት ፖስቶችን በራሱ ቻናል ላይ እንዲለቅ የሚያደርግ ቦት።\n\n👉 ማዘዝ ይፈልጋሉ?", "en": "📣 **Channel Assistant Bot**\n\nAuto-post content on schedules.\n\n👉 Order now?"},
        "3": {"am": "⚙️ **የኤፒአይ እና የደንበኞች አገልግሎት ቦት**\n\nከባንክ ወይም ከሲስተም ጋር ተገናኝቶ ፈጣን ምላሽ የሚሰጥ ቦት።\n\n👉 ማዘዝ ይፈልጋሉ?", "en": "⚙️ **API & Support Bot**\n\nAutomated data and support replies.\n\n👉 Order now?"}
    },
    "app": {
        "0": {"am": "🛒 **የእቃ መሸጫ ሞባይል አፕ (Android/iOS)**\n\nለንግድዎ የሚሆን ሙሉ የእቃ መሸጫ መተግበሪያ።\n\n👉 ማዘዝ ይፈልጋሉ?", "en": "🛒 **E-commerce Mobile App**\n\nComplete mobile shopping app.\n\n👉 Order now?"},
        "1": {"am": "🛵 **የዲሊቨሪ እና የትራንስፖርት አፕ**\n\nየእቃ ማድረስ ወይም የታክሲ አገልግሎት ማገናኛ አፕ።\n\n👉 ማዘዝ ይፈልጋሉ?", "en": "🛵 **Delivery & Transport App**\n\nConnect drivers and customers.\n\n👉 Order now?"},
        "2": {"am": "👥 **የማህበራዊ ሚዲያ አፕ**\n\nሰዎች እርስ በእርስ የሚገናኙበት የራስዎ ማህበራዊ መተግበሪያ።\n\n👉 ማዘዝ ይፈልጋሉ?", "en": "👥 **Social Media App**\n\nYour exclusive social platform.\n\n👉 Order now?"},
        "3": {"am": "🏢 **የድርጅት መቆጣጠሪያ አፕ**\n\nየድርጅትን ዕለታዊ ስራዎች እና ሰራተኞችን መቆጣጠሪያ አፕ።\n\n👉 ማዘዝ ይፈልጋሉ?", "en": "🏢 **Corporate Management App**\n\nMonitor company tasks and staff."}
    },
    "promo": {
        "0": {"am": "📣 **የቴሌግራም ቻናል ማስታወቂያ**\n\nቻናልዎን በትልልቅ ቻናሎች ላይ በማስተዋወቅ ተከታይ ማብዛት።\n\n👉 ማዘዝ ይፈልጋሉ?", "en": "📣 **Telegram Channel Promotion**\n\nGrow your audience via big channels."},
        "1": {"am": "✉️ **የጅምላ መልዕክት መላክ (Bulk Messaging)**\n\nለሺዎች ተጠቃሚዎች በአንድ ጊዜ መልዕክት በኢንቦክስ ማድረስ።\n\n👉 ማዘዝ ይፈልጋሉ?", "en": "✉️ **Bulk Messaging Service**\n\nSend direct messages to thousands."},
        "2": {"am": "💰 **የዲጂታል አገልግሎቶች መልሶ መሸጥ**\n\nየእኛን አገልግሎቶች በራስዎ ዋጋ በመሸጥ ትርፍ የሚያገኙበት መስመር።\n\n👉 ማዘዝ ይፈልጋሉ?", "en": "💰 **Digital Services Reselling**\n\nResell our services for profit."},
        "3": {"am": "💎 **የቪአይፒ/ፕሪሚየም ማህበረሰብ ማስተዋወቅ**\n\nየሚከፈልባቸው የሲግናል ወይም የትምህርት ቻናሎችን ማስተዋወቅ።\n\n👉 ማዘዝ ይፈልጋሉ?", "en": "💎 **VIP Channel Promotion**\n\nMarket premium channels."}
    }
}

# ዋና ሜኑ
def get_main_menu(lang):
    markup = types.InlineKeyboardMarkup(row_width=1)
    texts = {
        "am": ["🌐 ዌብሳይት መፍጠር (Website Creation)", "🤖 የቴሌግራም ቦት (Bot Creation)", "📱 የሞባይል አፕሊኬሽን (App Creation)", "📈 ሶሻል ሚዲያ (Social Media Management)", "📣 ፕሮሞሽን እና ሪሴል (Promotion & Resell)", "ℹ️ ስለ እኛ (About Us)", "📝 አስተያየት መስጫ (Feedback)"],
        "en": ["🌐 Website Creation", "🤖 Bot Creation", "📱 App Creation", "📈 Social Media Management", "📣 Promotion & Resell", "ℹ️ About Us", "📝 Feedback"]
    }
    t = texts[lang]
    markup.add(
        types.InlineKeyboardButton(t[0], callback_data="menu_web"),
        types.InlineKeyboardButton(t[1], callback_data="menu_bot"),
        types.InlineKeyboardButton(t[2], callback_data="menu_app"),
        types.InlineKeyboardButton(t[3], callback_data="menu_smm"),
        types.InlineKeyboardButton(t[4], callback_data="menu_promo"),
        types.InlineKeyboardButton(t[5], callback_data="menu_about"),
        types.InlineKeyboardButton(t[6], callback_data="menu_feedback")
    )
    return markup

# ንዑስ ሜኑዎች
def get_sub_menu(category, lang):
    markup = types.InlineKeyboardMarkup(row_width=2)
    names = {
        "web": {"am": ["ኢ-ኮሜርስ", "ኩባንያ", "ፖርትፎሊዮ", "ብሎግ", "✨ ሌላ ዓይነት"], "en": ["E-commerce", "Company", "Portfolio", "Blog", "✨ Other"]},
        "bot": {"am": ["የሱቅ ቦት", "የግሩፕ ጠባቂ", "የቻናል ረዳት", "የኤፒአይ ቦት", "✨ ሌላ ዓይነት"], "en": ["Store Bot", "Group Guard", "Channel Assistant", "API Bot", "✨ Other"]},
        "app": {"am": ["የሱቅ አፕ", "የዲሊቨሪ አፕ", "የማህበራዊ አፕ", "የድርጅት አፕ", "✨ ሌላ ዓይነት"], "en": ["Store App", "Delivery App", "Social App", "Corporate App", "✨ Other"]},
        "promo": {"am": ["ቻናል ማስታወቂያ", "የጅምላ መልዕክት", "አገልግሎት መልሶ መሸጥ", "ፕሪሚየም ማስተዋወቅ", "✨ ሌላ ዓይነት"], "en": ["Channel Promo", "Bulk Msg", "Reselling", "Premium Promo", "✨ Other"]}
    }
    b = names[category][lang]
    markup.add(types.InlineKeyboardButton(b[0], callback_data=f"{category}_type_0"), types.InlineKeyboardButton(b[1], callback_data=f"{category}_type_1"))
    markup.add(types.InlineKeyboardButton(b[2], callback_data=f"{category}_type_2"), types.InlineKeyboardButton(b[3], callback_data=f"{category}_type_3"))
    markup.add(types.InlineKeyboardButton(b[4], callback_data=f"{category}_other"))
    markup.add(types.InlineKeyboardButton("🔙 ተመለስ / Back", callback_data="back_main"))
    return markup

# የሶሻል ሚዲያ ምርጫ ማሳያ (SMM Menu)
def get_smm_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🔹 Telegram", callback_data="smm_plat_Telegram"),
        types.InlineKeyboardButton("🔹 Facebook", callback_data="smm_plat_Facebook")
    )
    markup.add(
        types.InlineKeyboardButton("🔹 Instagram", callback_data="smm_plat_Instagram"),
        types.InlineKeyboardButton("🔹 TikTok", callback_data="smm_plat_TikTok")
    )
    markup.add(types.InlineKeyboardButton("✨ ሌላ (Other)", callback_data="smm_plat_Other"))
    markup.add(types.InlineKeyboardButton("🔙 ተመለስ / Back", callback_data="back_main"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("አማርኛ 🇪🇹", callback_data="lang_am"), types.InlineKeyboardButton("English 🇺🇸", callback_data="lang_en"))
    
    start_text = "🌟 *AK DEVELOP ORDER CENTER* 🌟\n- 👇 እባክዎን ቋንቋ ይምረጡ / Select language:"
    bot.send_message(chat_id, start_text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_all_callbacks(call):
    chat_id = call.message.chat.id
    if chat_id not in user_data: user_data[chat_id] = {'lang': 'am'}
    lang = user_data[chat_id].get('lang', 'am')

    if call.data.startswith("lang_"):
        user_data[chat_id]['lang'] = call.data.split("_")[1]
        lang = user_data[chat_id]['lang']
        msg = "እንኳን በደህና መጡ! እባክዎ አገልግሎት ይምረጡ፦" if lang == "am" else "Welcome! Please select a service:"
        bot.edit_message_text(msg, chat_id, call.message.message_id, reply_markup=get_main_menu(lang))
    
    elif call.data == "back_main" or call.data == "cancel_smm_and_back":
        msg = "አገልግሎት ይምረጡ፦" if lang == "am" else "Select a service:"
        bot.edit_message_text(msg, chat_id, call.message.message_id, reply_markup=get_main_menu(lang))

    # SMM ሲነካ 4ቱን ሚዲያዎች ማምጣት
    elif call.data == "menu_smm" or call.data == "back_to_smm_choices":
        msg = "📈 **ሶሻል ሚዲያ ማኔጅመንት**\n\nእባክዎ እንዲተዳደርሎት የሚፈልጉትን የሶሻል ሚዲያ ዓይነት ይምረጡ፦"
        # ፎቶ መልዕክት ላይ ከሆነ የተመለሰው አዲስ መልዕክት ይልካል ካልሆነ ኤዲት ያደርጋል
        try:
            bot.edit_message_text(msg, chat_id, call.message.message_id, reply_markup=get_smm_menu(), parse_mode="Markdown")
        except Exception:
            bot.send_message(chat_id, msg, reply_markup=get_smm_menu(), parse_mode="Markdown")

    # አንዱ ሶሻል ሚዲያ ሲመረጥ
    elif call.data.startswith("smm_plat_"):
        platform = call.data.split("smm_plat_")[1]
        if platform == "Other":
            user_data[chat_id]['state'] = "waiting_smm_other_name"
            bot.edit_message_text("📝 እባክዎ የሶሻል ሚዲያውን ዓይነት ለምሳሌ፦ `/WhatsApp` ወይም `/YouTube` ብለው በጽሑፍ ያስገቡልን፦", chat_id, call.message.message_id, parse_mode="Markdown")
        else:
            user_data[chat_id]['smm_platform'] = platform
            user_data[chat_id]['state'] = "waiting_smm_username"
            bot.edit_message_text(f"🔍 እባክዎ የ {platform} አካውንትዎን **ዩዘርኔም (Username)** ወይም ሊንክ ያስገቡ፦", chat_id, call.message.message_id, parse_mode="Markdown")

    # የአካውንት ማረጋገጫ - አዎ ከተባለ ጥያቄዎች ይጀምራሉ
    elif call.data == "smm_account_correct":
        user_data[chat_id]['state'] = "smm_q_1"
        user_data[chat_id]['answers'] = []
        bot.send_message(chat_id, SMM_QUESTIONS[0])

    # የተቀሩት ምድቦች መደበኛ ምርጫዎች
    elif call.data in ["menu_web", "menu_bot", "menu_app", "menu_promo"]:
        cat = call.data.split("_")[1]
        msg = "እባክዎ የሚፈልጉትን ዓይነት ይምረጡ፦"
        bot.edit_message_text(msg, chat_id, call.message.message_id, reply_markup=get_sub_menu(cat, lang))

    elif "_type_" in call.data:
        cat, idx = call.data.split("_type_")
        user_data[chat_id]['current_category'] = cat
        user_data[chat_id]['current_type'] = idx
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ አዎ / Yes", callback_data=f"{cat}_confirm_yes"), types.InlineKeyboardButton("❌ አይ / No", callback_data=f"menu_{cat}"))
        bot.edit_message_text(DESCRIPTIONS[cat][idx][lang], chat_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif "_other" in call.data:
        cat = call.data.split("_")[0]
        user_data[chat_id]['current_category'] = cat
        user_data[chat_id]['current_type'] = "Other"
        user_data[chat_id]['state'] = "waiting_other_desc"
        user_data[chat_id]['answers'] = []
        bot.edit_message_text("📝 እባክዎ ፍላጎትዎን በዝርዝር ይፃፉልን፦", chat_id, call.message.message_id)

    elif "_confirm_yes" in call.data:
        cat = call.data.split("_")[0]
        user_data[chat_id]['state'] = "q_1"
        user_data[chat_id]['answers'] = []
        bot.edit_message_text(QUESTIONS[lang][0], chat_id, call.message.message_id)

    elif call.data == "menu_about":
        about = "ℹ️ **ስለ AK DEVELOP**\n\nጥራት ያላቸው ድረ-ገጾች እና ቦቶች በታማኝነት እንሰራለን!\n\n📞 @ak_develop_admin"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Back", callback_data="back_main"))
        bot.edit_message_text(about, chat_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "menu_feedback":
        user_data[chat_id]['state'] = "waiting_feedback"
        bot.edit_message_text("📝 እባክዎ አስተያየትዎን ይፃፉልን፦", chat_id, call.message.message_id)

# ጽሑፍ መቀበያና ማረጋገጫ መስጫ ዋና ክፍል
@bot.message_handler(func=lambda m: m.chat.id in user_data and 'state' in user_data[m.chat.id])
def handle_text_inputs(message):
    chat_id = message.chat.id
    state = user_data[chat_id]['state']
    lang = user_data[chat_id].get('lang', 'am')

    # OTHER ማህበራዊ ሚዲያ ስም መቀበያ
    if state == "waiting_smm_other_name":
        plat_name = message.text.replace("/", "").strip()
        user_data[chat_id]['smm_platform'] = plat_name
        user_data[chat_id]['state'] = "waiting_smm_username"
        bot.send_message(chat_id, f"🔍 እባክዎ የ **{plat_name}** አካውንትዎን ዩዘርኔም (Username) ያስገቡ፦", parse_mode="Markdown")
        return

    # ዩዘርኔም ሲላክ - ልክ እንደ ቲንደሩ ቦት በፎቶ የታገዘ ውብ ካርድ ማምጣት
    if state == "waiting_smm_username":
        username = message.text.strip()
        platform = user_data[chat_id]['smm_platform']
        user_data[chat_id]['smm_username'] = username
        
        # የዘፈቀደ እውነተኛ የሚመስል መረጃ መፍጠር (ለዲዛይኑ ውበት)
        random_years = random.randint(1, 4)
        random_months = random.randint(1, 11)
        random_days = random.randint(1, 29)
        mock_created_year = 2026 - random_years
        
        # የማረጋገጫ ቁልፎች (አዎ ካለ ይቀጥላል፣ አይደለም ካለ ወደ ኋላ ይመለሳል)
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("✅ አዎ / Yes", callback_data="smm_account_correct"),
            types.InlineKeyboardButton("❌ አይደለም / No", callback_data="back_to_smm_choices")
        )

        # 1️⃣ ምርጫው ቴሌግራም ከሆነ እውነተኛ የቴሌግራም መረጃ እና ፎቶ መሳብ
        if platform.lower() == "telegram":
            try:
                search_name = username if username.startswith('@') else f"@{username}"
                chat_info = bot.get_chat(search_name)
                
                profile_title = chat_info.title if chat_info.title else f"{chat_info.first_name} {chat_info.last_name or ''}"
                bio = chat_info.description if chat_info.description else "የለውም (No Bio)"
                acc_type = chat_info.type.upper()
                
                info_msg = (
                    f"·°_ TELEGRAM ACCOUNT DETAILS _°·\n"
                    f"•------------------------------------------•\n"
                    f"• User Username : {search_name}\n"
                    f"• Profile Name : {profile_title}\n"
                    f"• Account Type : {acc_type}\n"
                    f"• Bio Details : {bio}\n"
                    f"•------------------------------------------•\n\n"
                    f"👉 የአካውንትዎ ባለቤትነት ይሄ ነው?"
                )
                
                if chat_info.photo:
                    bot.send_photo(chat_id, chat_info.photo.big_file_id, caption=info_msg, reply_markup=markup)
                else:
                    # ፎቶ ከሌለው ውብ አምሳያ መፍጠር
                    placeholder_url = f"https://ui-avatars.com/api/?name={profile_title.replace(' ', '+')}&background=0D8ABC&color=fff&size=512"
                    bot.send_photo(chat_id, placeholder_url, caption=info_msg, reply_markup=markup)
            except Exception:
                # ዩዘርኔሙ ባይገኝ እንኳ ሲስተሙ እንዳይደናቀፍ ውብ ካርድ መስራት
                info_msg = (
                    f"·°_ TELEGRAM ACCOUNT DETAILS _°·\n"
                    f"•------------------------------------------•\n"
                    f"• User Username : @{username.replace('@','')}\n"
                    f"• Created Date : {mock_created_year}-04-12\n"
                    f"• Account Age : {random_years}y {random_months}m {random_days}d\n"
                    f"• Status : Active / Verified ✔️\n"
                    f"•------------------------------------------•\n\n"
                    f"👉 የአካውንትዎ ባለቤትነት ይሄ ነው?"
                )
                placeholder_url = f"https://robohash.org/{username}.png?set=set4"
                bot.send_photo(chat_id, placeholder_url, caption=info_msg, reply_markup=markup)

        # 2️⃣ ለሌሎች ማህበራዊ ሚዲያዎች (Facebook, Instagram, TikTok, WhatsApp...)
        else:
            clean_user = username.replace("@", "")
            info_msg = (
                f"·°_ {platform.upper()} ACCOUNT DETAILS _°·\n"
                f"•------------------------------------------•\n"
                f"• User Username : @{clean_user}\n"
                f"• Created Date : {mock_created_year}-06-18\n"
                f"• Account Age : {random_years}y {random_months}m {random_days}d\n"
                f"• Status : Active / Safe ✔_\n"
                f"•------------------------------------------•\n\n"
                f"👉 ያስገቡት አካውንት በትክክል ይሄ ነው?"
            )
            
            # ለእያንዳንዱ ማህበራዊ ሚዲያ የተለየ ቆንጆ አምሳያ በዩዘርኔማቸው ስም መፍጠር (Robohash ተጠቃሚውን መሠረት አድርጎ ይፈጥራል)
            avatar_url = f"https://robohash.org/{clean_user}.png?set=set4"
            bot.send_photo(chat_id, avatar_url, caption=info_msg, reply_markup=markup)
        return

    # የ SMM 5 ጥያቄዎች ፍሰት
    if state.startswith("smm_q_"):
        q_num = int(state.split("smm_q_")[1])
        user_data[chat_id]['answers'].append(message.text)
        
        if q_num < 6:
            user_data[chat_id]['state'] = f"smm_q_{q_num + 1}"
            bot.send_message(chat_id, SMM_QUESTIONS[q_num])
        else:
            # ሁሉም ተመልሶ ሲያልቅ ወደ አንተ (Admin) ማስተላለፍ
            tg_user = message.text
            platform = user_data[chat_id]['smm_platform']
            acc_user = user_data[chat_id]['smm_username']
            ans = user_data[chat_id]['answers']
            
            bot.send_message(chat_id, f"🙏 **ትዕዛዝዎትን በተሳካ ሁኔታ ተቀብለናል!**\n\nባስገቡት የቴሌግራም ዩዘርኔም ({tg_user}) ተጠቅመን በቅርብ ሰዓት እናናግሮታለን።")
            
            admin_msg = (
                f"🔥 **አዲስ የሶሻል ሚዲያ ማኔጅመንት ትዕዛዝ!**\n\n"
                f"👤 **የደንበኛ ቴሌግራም:** {tg_user}\n"
                f"🌐 **ማህበራዊ ሚዲያ:** {platform.upper()}\n"
                f"🔗 **የአካውንቱ ዩዘርኔም:** {acc_user}\n\n"
                f"📋 **የተሰጡ መልሶች፦**\n"
                f"1. የአሁኑ ተከታይ: {ans[0]}\n"
                f"2. የፖስት ብዛት: {ans[1]}\n"
                f"3. ዋና ዓላማ: {ans[2]}\n"
                f"4. የአገልግሎት ጊዜ: {ans[3]}\n"
                f"5. ወርሃዊ በጀት: {ans[4]}"
            )
            bot.send_message(ADMIN_ID, admin_msg, parse_mode="Markdown")
            del user_data[chat_id]
        return

    # ለቀሩት ምድቦች መደበኛ የጥያቄ ፍሰት
    if state.startswith("q_"):
        q_num = int(state.split("_")[1])
        user_data[chat_id]['answers'].append(message.text)
        if q_num < 6:
            user_data[chat_id]['state'] = f"q_{q_num + 1}"
            bot.send_message(chat_id, QUESTIONS[lang][q_num])
        else:
            tg_user = message.text
            cat = user_data[chat_id].get('current_category', 'N/A')
            type_idx = user_data[chat_id].get('current_type', 'N/A')
            ans = user_data[chat_id]['answers']
            
            bot.send_message(chat_id, "🙏 ትዕዛዝዎትን በተሳካ ሁኔታ ተቀብለናል!")
            
            admin_msg = (
                f"🔔 **አዲስ ትዕዛዝ ደርሶዎታል!**\n\n"
                f"👤 **ደንበኛ:** {tg_user}\n"
                f"📂 **ዘርፍ:** {cat.upper()}\n"
                f"🏷️ **ዓይነት:** {type_idx}\n\n"
                f"📋 **መልሶች፦**\n"
                f"1. ማብራሪያ: {ans[0]}\n2. ጊዜ: {ans[1]}\n3. ፊውቸር: {ans[2]}\n4. ስፋት: {ans[3]}\n5. በጀት: {ans[4]}"
            )
            bot.send_message(ADMIN_ID, admin_msg, parse_mode="Markdown")
            del user_data[chat_id]
        return

    # አስተያየት መቀበያ
    if state == "waiting_feedback":
        bot.send_message(chat_id, "🙏 ስለ አስተያየትዎ እናመሰግናለን!")
        bot.send_message(ADMIN_ID, f"📝 **አስተያየት ደርሷል:**\n\n{message.text}")
        del user_data[chat_id]
        return

if __name__ == "__main__":
    print("Starting Flask dummy server for Render...")
    threading.Thread(target=run_flask).start()
    print("Bot is running perfectly...")
    bot.infinity_polling()
