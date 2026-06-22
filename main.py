import telebot
from telebot import types

# 1. ቦቱን በአዲሱ ቶከን ማስጀመር
TOKEN = "8995958985:AAFsOQ1SxWmTe6gGo-lBFXAv72YjHAWLHBQ"
ADMIN_ID = "8926052749"
bot = telebot.TeleBot(TOKEN)

# የደንበኞች መረጃ ጊዜያዊ ማከማቻ (State Management)
user_data = {}

# የ 5ቱ ረጅም ጥያቄዎች ዝርዝር (ለዌብሳይት፣ ቦት እና አፕ)
QUESTIONS = {
    "am": [
        "1️⃣ ለመሆኑ ይህ ሲስተም እንዴት እንዲሰራሎት ይፈልጋሉ? እባክዎ ሙሉ ፍላጎቶትን በዝርዝር ይፃፉልን፦",
        "2️⃣ ፕሮጀክቱ ተጠናቆ እንዲረከቡ የሚፈልጉት እስከ መቼ ነው? (የጊዜ ገደብ/Deadline)፦",
        "3️⃣ በፕሮጀክቱ ውስጥ እንዲካተቱ የሚፈልጓቸው ልዩ አገልግሎቶች ወይም ገፅታዎች (Features) ምንድን ናቸው?፦",
        "4️⃣ ይህ ሲስተም ምን ያህል ገፆች (Pages) ወይም ንዑስ ክፍሎች እንዲኖሩት ይገምታሉ?፦",
        "5️⃣ ለዚህ ስራ የመደቡት ግምታዊ በጀት (Budget) በኢትዮጵያ ብር ምን ያህል ነው?፦",
        "🎯 በመጨረሻም፣ የእርስዎን የቴሌግራም ዩዘርኔም (ለምሳሌ @username) ያስገቡ፦"
    ],
    "en": [
        "1️⃣ How exactly do you want this system to work? Please describe your requirements in detail:",
        "2️⃣ When do you need this project to be completed? (Target Deadline):",
        "3️⃣ What specific features or functionalities should be included in the system?:",
        "4️⃣ How many pages or sub-sections do you estimate this system will have?:",
        "5️⃣ What is your estimated budget in ETB for this project?:",
        "🎯 Finally, please enter your Telegram username (e.g., @username):"
    ]
}

# የእያንዳንዱ ምርጫ ረጅም እና ዝርዝር መግለጫዎች
DESCRIPTIONS = {
    "web": {
        "0": {
            "am": "🛍️ **የኢ-ኮሜርስ (ኦንላይን ገበያ) ድረ-ገጽ**\n\nይህ የንግድ ድርጅትዎን ምርቶች በምስል፣ በዋጋ እና በዝርዝር መግለጫ ለደንበኛ የሚያቀርቡበት ዘመናዊ መድረክ ነው። ደንበኞች በቤታቸው ሆነው በቀላሉ እንዲገበዩ እና በቴሌግራም ወይም በባንክ ክፍያ ትዕዛዝ እንዲልኩ ያደርጋል።\n\n👉 ይህንን አገልግሎት ማዘዝ ይፈልጋሉ?",
            "en": "🛍️ **E-commerce Website**\n\nThis is a modern platform to showcase your business products with images, prices, and descriptions. It allows customers to easily shop from home and send orders via Telegram or bank transfer.\n\n👉 Do you want to order this service?"
        },
        "1": {
            "am": "💼 **የኩባንያ/ቢዝነስ ማስተዋወቂያ ድረ-ገጽ**\n\nየድርጅትዎን አገልግሎቶች፣ አድራሻ፣ ራዕይ እና የስራ ታሪክ ለደንበኞች በፕሮፌሽናል መልክ የሚያስተዋውቁበት ነው። የቢዝነስዎን ተዓማኒነት ለመጨመር እና አዳዲስ ደንበኞችን ለመሳብ እጅግ በጣም አስፈላጊ ነው።\n\n👉 ይህንን አገልግሎት ማዘዝ ይፈልጋሉ?",
            "en": "💼 **Business/Company Website**\n\nA platform to professionally showcase your organization's services, location, vision, and history. Crucial for building business credibility and attracting new clients.\n\n👉 Do you want to order this service?"
        },
        "2": {
            "am": "🎨 **የግል ሥራ ማሳያ (Portfolio) ድረ-ገጽ**\n\nየግል ሙያዎን፣ የተማሩትን ትምህርት እና እስካሁን የሰሯቸውን ምርጥ ስራዎች ለአሰሪዎች እና ለደንበኞች ውብ በሆነ አቀራረብ የሚያሳዩበት ገጽ ነው። ለፍሪላንሰሮች እና ባለሙያዎች ተመራጭ ነው።\n\n👉 ይህንን አገልግሎት ማዘዝ ይፈልጋሉ?",
            "en": "🎨 **Portfolio Website**\n\nA beautiful showcase page to display your professional skills, education, and past projects to employers and clients. Highly recommended for freelancers and professionals.\n\n👉 Do you want to order this service?"
        },
        "3": {
            "am": "📝 **የብሎግ እና መረጃ ሰጪ ድረ-ገጽ**\n\nየተለያዩ ፅሁፎችን፣ ዜናዎችን፣ ትምህርታዊ መረጃዎችን ወይም የግል እይታዎችን በየቀኑ ለተከታዮችዎ የሚያጋሩበት፣ ሰፊ ማህበረሰብ የሚገነቡበት እና ከማስታወቂያ ገቢ የሚያገኙበት ድረ-ገጽ ነው።\n\n👉 ይህንን አገልግሎት ማዘዝ ይፈልጋሉ?",
            "en": "📝 **Blog & Informational Website**\n\nA website to share articles, news, educational content, or personal views daily with your audience, build a community, and generate ad revenue.\n\n👉 Do you want to order this service?"
        }
    },
    "bot": {
        "0": {
            "am": "🏪 **የቴሌግራም የሱቅ/መሸጫ ቦት (Store Bot)**\n\nደንበኞች ከቴሌግራም ሳይወጡ ምርቶችዎን አይተው፣ መርጠው፣ በቅርጫት (Cart) አክለው በቀጥታ እንዲገዙ እና ትዕዛዝ ወደ እርስዎ እንዲመጣ የሚያደርግ እጅግ ፈጣን አውቶማቲክ ቦት ነው።\n\n👉 ይህንን አገልግሎት ማዘዝ ይፈልጋሉ?",
            "en": "🏪 **Telegram Store Bot**\n\nA fast automatic bot allowing customers to browse products, add to cart, and checkout directly within Telegram, sending the order straight to you.\n\n👉 Do you want to order this service?"
        },
        "1": {
            "am": "🛡️ **የግሩፕ ማኔጅመንት እና ጥበቃ ቦት**\n\nየቴሌግራም ግሩፖችን ከአላስፈላጊ ሊንኮች፣ ስድቦች፣ ስፓም ሜሴጆች እና ከአጭበርባሪዎች በ24 ሰዓት ሙሉ በራስ-ሰር የሚጠብቅ እና አባላትን በአግባቡ የሚያስተዳድር የቁጥጥር ቦት ነው።\n\n👉 ይህንን አገልግሎት ማዘዝ ይፈልጋሉ?",
            "en": "🛡️ **Group Management Bot**\n\nA control bot that automatically protects Telegram groups from unwanted links, insults, spam messages, and scammers 24/7, while efficiently managing members.\n\n👉 Do you want to order this service?"
        },
        "2": {
            "am": "📣 **የቻናል እና የይዘት ማሰራጫ ቦት (Content Bot)**\n\nበተዋቀረ ሰዓት ፖስቶችን በራሱ ቻናል ላይ እንዲለቅ፣ ማስታወቂያዎችን እንዲያስተዳድር እና ከተከታዮች የሚመጡ መልዕክቶችን በስርዓት እንዲቀበል የሚያስችል ረዳት ቦት ነው።\n\n👉 ይህንን አገልግሎት ማዘዝ ይፈልጋሉ?",
            "en": "📣 **Channel & Content Distribution Bot**\n\nAn assistant bot capable of auto-posting content at scheduled times, managing advertisements, and systematically handling feedback from followers.\n\n👉 Do you want to order this service?"
        },
        "3": {
            "am": "⚙️ **የኤፒአይ (API Integration) እና የደንበኞች አገልግሎት ቦት**\n\nከሌሎች ሲስተሞች (ባንኮች፣ ዌብሳይቶች) ጋር በመገናኘት አውቶማቲክ መረጃዎችን የሚሰጥ ወይም ለደንበኞች ፈጣን ምላሽ (Customer Support) የሚሰጥ የተራቀቀ ቦት ነው።\n\n👉 ይህንን አገልግሎት ማዘዝ ይፈልጋሉ?",
            "en": "⚙️ **API Integration & Support Bot**\n\nAn advanced bot connected with external systems (banks, websites) to provide automated data or deliver instant customer support replies.\n\n👉 Do you want to order this service?"
        }
    },
    "app": {
        "0": {
            "am": "🛒 **የእቃ መሸጫ ሞባይል አፕሊኬሽን (Android/iOS)**\n\nለንግድዎ የሚሆን ሙሉ መተግበሪያ ሲሆን ደንበኞች በስልካቸው ጭነው ምርቶችዎን የሚገበዩበት፣ የትዕዛዝ ሁኔታቸውን የሚከታተሉበት እና ማሳወቂያዎች (Push Notifications) የሚደርሳቸው መተግበሪያ ነው።\n\n👉 ይህንን አገልግሎት ማዘዝ ይፈልጋሉ?",
            "en": "🛒 **E-commerce Mobile App (Android/iOS)**\n\nA complete mobile application for your business where customers install it to shop, track order status, and receive direct push notifications.\n\n👉 Do you want to order this service?"
        },
        "1": {
            "am": "🛵 **የዲሊቨሪ እና የትራንስፖርት አገልግሎት አፕ**\n\nየእቃ ማድረስ፣ የቤት ለቤት ምግብ አቅርቦት ወይም የትራንስፖርት/ታክሲ አገልግሎት የሚሰጡ ድርጅቶች ሹፌሮችን እና ደንበኞችን በአንድ ላይ የሚያገናኙበት ዘመናዊ መተግበሪያ ነው።\n\n👉 ይህንን አገልግሎት ማዘዝ ይፈልጋሉ?",
            "en": "🛵 **Delivery & Transport Service App**\n\nA modern application connecting drivers and customers for delivery, home food supply, or transport/taxi service companies.\n\n👉 Do you want to order this service?"
        },
        "2": {
            "am": "👥 **የማህበራዊ ሚዲያ እና የኮሚኒቲ አፕ**\n\nሰዎች እርስ በእርስ የሚገናኙበት፣ ፎቶ እና ቪዲዮ የሚጋሩበት፣ የሚወያዩበት እና የራሶን የተለየ ማህበረሰብ የሚገነቡበት የራስዎ ብቸኛ ማህበራዊ መተግበሪያ ነው።\n\n👉 ይህንን አገልግሎት ማዘዝ ይፈልጋሉ?",
            "en": "👥 **Social Media & Community App**\n\nYour exclusive social platform where people connect, share photos and videos, chat, and build a unique community under your brand.\n\n👉 Do you want to order this service?"
        },
        "3": {
            "am": "🏢 **የድርጅት መቆጣጠሪያ እና ሰራተኞች አፕ**\n\nየድርጅቶን ዕለታዊ ስራዎች፣ የሰራተኞች ክትትል፣ የፋይናንስ ሁኔታ እና ሪፖርቶችን በአንድ ቦታ ሆነው በስልኮት በቀላሉ ለመቆጣጠር የሚያስችል የውስጥ አፕሊኬሽን ነው።\n\n👉 ይህንን አገልግሎት ማዘዝ ይፈልጋሉ?",
            "en": "🏢 **Corporate & Staff Management App**\n\nAn internal application that allows you to easily monitor daily company tasks, employee attendance, finances, and reports directly from your phone.\n\n👉 Do you want to order this service?"
        }
    }
}

# ዋና ሜኑ
def get_main_menu(lang):
    markup = types.InlineKeyboardMarkup(row_width=1)
    texts = {
        "am": [
            "🌐 ዌብሳይት መፍጠር (Website Creation)", "🤖 የቴሌግራም ቦት (Bot Creation)", 
            "📱 የሞባይል አፕሊኬሽን (App Creation)", "📈 ሶሻል ሚዲያ (Social Media Management)", 
            "📣 ፕሮሞሽን እና ሪሴል (Promotion & Resell)", "ℹ️ ስለ እኛ (About Us)", "📝 አስተያየት መስጫ (Feedback)"
        ],
        "en": [
            "🌐 Website Creation", "🤖 Bot Creation", "📱 App Creation", 
            "📈 Social Media Management", "📣 Promotion & Resell", "ℹ️ About Us", "📝 Feedback"
        ]
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

# ንዑስ ሜኑዎች (ዌብሳይት፣ ቦት፣ አፕ)
def get_sub_menu(category, lang):
    markup = types.InlineKeyboardMarkup(row_width=2)
    names = {
        "web": {
            "am": ["ኢ-ኮሜርስ", "ኩባንያ", "ፖርትፎሊዮ", "ብሎግ", "✨ ሌላ ዓይነት (Other)"],
            "en": ["E-commerce", "Company", "Portfolio", "Blog", "✨ Other Type"]
        },
        "bot": {
            "am": ["የሱቅ ቦት", "የግሩፕ ጠባቂ", "የቻናል ረዳት", "የኤፒአይ ቦት", "✨ ሌላ ዓይነት (Other)"],
            "en": ["Store Bot", "Group Guard", "Channel Assistant", "API Bot", "✨ Other Type"]
        },
        "app": {
            "am": ["የሱቅ አፕ", "የዲሊቨሪ አፕ", "የማህበራዊ አፕ", "የድርጅት አፕ", "✨ ሌላ ዓይነት (Other)"],
            "en": ["Store App", "Delivery App", "Social App", "Corporate App", "✨ Other Type"]
        }
    }
    b = names[category][lang]
    markup.add(
        types.InlineKeyboardButton(b[0], callback_data=f"{category}_type_0"),
        types.InlineKeyboardButton(b[1], callback_data=f"{category}_type_1")
    )
    markup.add(
        types.InlineKeyboardButton(b[2], callback_data=f"{category}_type_2"),
        types.InlineKeyboardButton(b[3], callback_data=f"{category}_type_3")
    )
    markup.add(types.InlineKeyboardButton(b[4], callback_data=f"{category}_other"))
    markup.add(types.InlineKeyboardButton("🔙 ተመለስ / Back", callback_data="back_main"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("አማርኛ 🇪🇹", callback_data="lang_am"),
               types.InlineKeyboardButton("English 🇺🇸", callback_data="lang_en"))
    
    start_text = (
        "🌟 *AK DEVELOP ORDER CENTER* 🌟\n"
        "- 🚀 የእርስዎ የዲጂታል አገልግሎት ማዕከል! / Your digital service hub!\n"
        "- 🌐 ጥራት ያለው የዌብሳይትና የቦት ስራዎች! / Quality Website & Bot services!\n"
        "- ⚡ ፈጣን እና አስተማማኝ ድጋፍ እንሰጣለን! / Fast & reliable support!\n"
        "- 👇 እባክዎን የሚፈልጉትን ቋንቋ ይምረጡ / Please select your language:"
    )
    bot.send_message(chat_id, start_text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_all_callbacks(call):
    chat_id = call.message.chat.id
    
    if chat_id not in user_data:
        user_data[chat_id] = {'lang': 'am'}
    lang = user_data[chat_id].get('lang', 'am')

    # የቋንቋ ምርጫ
    if call.data.startswith("lang_"):
        user_data[chat_id]['lang'] = call.data.split("_")[1]
        lang = user_data[chat_id]['lang']
        msg = "እንኳን በደህና መጡ! እባክዎ ከታች ካሉት ዋና ዋና አገልግሎቶቻችን ውስጥ ፍላጎትዎን ይምረጡ፦" if lang == "am" else "Welcome! Please select your desired service from our main services below:"
        bot.edit_message_text(msg, chat_id, call.message.message_id, reply_markup=get_main_menu(lang))
    
    # ወደ ዋና ሜኑ መመለሻ
    elif call.data == "back_main":
        msg = "አገልግሎት ይምረጡ፦" if lang == "am" else "Select a service:"
        bot.edit_message_text(msg, chat_id, call.message.message_id, reply_markup=get_main_menu(lang))

    # ዋና ምድቦች ሲመረጡ (Web, Bot, App)
    elif call.data == "menu_web":
        msg = "እባክዎ ሊሰራልዎት የሚፈልጉትን የዌብሳይት ዓይነት ይምረጡ፦" if lang == "am" else "Please select the type of website you want to build:"
        bot.edit_message_text(msg, chat_id, call.message.message_id, reply_markup=get_sub_menu("web", lang))
        
    elif call.data == "menu_bot":
        msg = "እባክዎ ሊሰራልዎት የሚፈልጉትን የቦት ዓይነት ይምረጡ፦" if lang == "am" else "Please select the type of bot you want to build:"
        bot.edit_message_text(msg, chat_id, call.message.message_id, reply_markup=get_sub_menu("bot", lang))

    elif call.data == "menu_app":
        msg = "እባክዎ ሊሰራልዎት የሚፈልጉትን የአፕሊኬሽን ዓይነት ይምረጡ፦" if lang == "am" else "Please select the type of application you want to build:"
        bot.edit_message_text(msg, chat_id, call.message.message_id, reply_markup=get_sub_menu("app", lang))

    # አንዱ ዓይነት ሲመረጥ (የረጅም መግለጫ ማሳያ)
    elif "_type_" in call.data:
        parts = call.data.split("_type_")
        category = parts[0]
        type_idx = parts[1]
        
        user_data[chat_id]['current_category'] = category
        user_data[chat_id]['current_type'] = type_idx
        
        desc_text = DESCRIPTIONS[category][type_idx][lang]
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ አዎ / Yes", callback_data=f"{category}_confirm_yes"),
                   types.InlineKeyboardButton("❌ አይ / No", callback_data=f"menu_{category}"))
        bot.edit_message_text(desc_text, chat_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    # "ሌላ (Other)" ሲመረጥ
    elif "_other" in call.data:
        category = call.data.split("_")[0]
        user_data[chat_id]['current_category'] = category
        user_data[chat_id]['current_type'] = "Other"
        user_data[chat_id]['state'] = "waiting_other_desc"
        user_data[chat_id]['answers'] = []
        
        msg = "📝 እባክዎ ሊሰራልዎት ያሰቡትን ፕሮጀክት ምንነት እና ምን ምን ነገሮችን ማካተት እንዳለበት በዝርዝር ይፃፉልን፦" if lang == "am" else "📝 Please describe what kind of project you want to build and what features it should include in detail:"
        bot.edit_message_text(msg, chat_id, call.message.message_id)

    # አዎ ተብሎ ጥያቄዎች ሲጀምሩ
    elif "_confirm_yes" in call.data:
        category = call.data.split("_")[0]
        user_data[chat_id]['state'] = "q_1"
        user_data[chat_id]['answers'] = []
        
        bot.edit_message_text(QUESTIONS[lang][0], chat_id, call.message.message_id)

# የተጠቃሚ መልሶችን (ጽሑፎችን) መቀበያ
@bot.message_handler(func=lambda m: m.chat.id in user_data and 'state' in user_data[m.chat.id])
def handle_user_answers(message):
    chat_id = message.chat.id
    lang = user_data[chat_id].get('lang', 'am')
    state = user_data[chat_id]['state']
    
    # የ Other መግለጫ መጀመሪያ ከተጻፈ
    if state == "waiting_other_desc":
        user_data[chat_id]['answers'].append(message.text)
        user_data[chat_id]['state'] = "q_2" # የ መጀመሪያውን ጥያቄ ስለመለሱ ቀጥታ ወደ 2ኛው ያልፋል
        bot.send_message(chat_id, QUESTIONS[lang][1])
        return

    # መደበኛ ጥያቄዎችን ማስተናገድ
    if state.startswith("q_"):
        current_q_num = int(state.split("_")[1])
        user_data[chat_id]['answers'].append(message.text)
        
        if current_q_num < 6:
            user_data[chat_id]['state'] = f"q_{current_q_num + 1}"
            bot.send_message(chat_id, QUESTIONS[lang][current_q_num])
        else:
            # ሁሉም ተሞልቶ ሲያልቅ - ለደንበኛው ማረጋገጫ መስጠት
            username = message.text
            thanks_msg = (
                f"🙏 **ትዕዛዝዎትን በተሳካ ሁኔታ ተቀብለናል!**\n\n"
                f"ባስገቡት የቴሌግራም ዩዘርኔም ({username}) ተጠቅመን በቅርብ ሰዓት ውስጥ በውስጥ መስመር እናናግሮታለን። ስላናገሩን እናመሰግናለን!"
                if lang == "am" else
                f"🙏 **Order successfully received!**\n\n"
                f"We will contact you shortly via your Telegram username ({username}). Thank you for choosing us!"
            )
            bot.send_message(chat_id, thanks_msg, parse_mode="Markdown")
            
            # ለአንተ (Admin) መረጃውን መላክ
            category = user_data[chat_id].get('current_category', 'N/A')
            type_idx = user_data[chat_id].get('current_type', 'N/A')
            answers = user_data[chat_id]['answers']
            
            admin_msg = (
                f"🔔 **አዲስ ትዕዛዝ ደርሶዎታል!**\n\n"
                f"👤 **ደንበኛ (Username):** {username}\n"
                f"📂 **የአገልግሎት ዘርፍ:** {category.upper()}\n"
                f"🏷️ **የመረጡት ዓይነት:** {type_idx}\n\n"
                f"📋 **የተሰጡ መልሶች፦**\n"
                f"1. ማብራሪያ: {answers[0]}\n"
                f"2. የጊዜ ገደብ: {answers[1]}\n"
                f"3. ልዩ ፊውቸሮች: {answers[2]}\n"
                f"4. የገፅ ብዛት: {answers[3]}\n"
                f"5. በጀት: {answers[4]}"
            )
            bot.send_message(ADMIN_ID, admin_msg, parse_mode="Markdown")
            
            # ስቴቱን ማጽዳት
            del user_data[chat_id]

if __name__ == "__main__":
    print("Bot is running perfectly...")
    bot.infinity_polling()
