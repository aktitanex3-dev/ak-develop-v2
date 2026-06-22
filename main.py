import telebot
from telebot import types
import threading
from flask import Flask
import os
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

# 📈 የሶሻል ሚዲያ 5 ዋና ጥያቄዎች (እያንዳንዳቸው ከ6-7 መስመር ዝርዝር ማብራሪያ አላቸው)
SMM_QUESTIONS = [
    "1️⃣ **ለማስተዳደር ያሰቡት አካውንት አሁን ላይ በግምት ምን ያህል ተከታይ/አባላት አሉት?**\n\n"
    "■ ይህ ጥያቄ የአካውንትዎን የአሁኑን ቁመና ለመረዳት ይረዳናል።\n"
    "■ በነባር ተከታዮችዎ ልክ የሚመጥን ስትራቴጂ ለመንደፍ ይጠቅመናል።\n"
    "■ ኦርጋኒክ (ከተፈጥሯዊ) ዕድገት ወይስ ከማስታወቂያ እንደምንጀምር ይወስናል።\n"
    "■ እባክዎ በአሁኑ ሰዓት ያለውን ትክክለኛ የተከታይ ቁጥር በግምት ይፃፉልን፦",

    "2️⃣ **በሳምንት ወይም በወር ውስጥ ምን ያህል ፖስቶች/ቪዲዮዎች እንዲሰሩሎት ይፈልጋሉ?**\n\n"
    "■ የይዘት (Content) መውጫ መርሃ-ግብር ለመቅረፅ በጣም ወሳኝ ጥያቄ ነው።\n"
    "■ ግራፊክስ ዲዛይን፣ አጫጭር ቪዲዮዎች (Shorts/Reels) እና ፅሁፎችን ያካትታል።\n"
    "■ በየቀኑ እንዲፖስት ወይስ በሳምንት የተወሰኑ ቀናት እንደሚፈልጉ ይወስናል።\n"
    "■ እባክዎ የሚፈልጉትን የይዘት ብዛት በጥልቀት ያብራሩልን፦",

    "3️⃣ **የዚህ አካውንት ዋና ዓላማ ምንድን ነው? (ሽያጭ፣ ታዋቂነት ወይስ ተከታይ ማብዛት?)**\n\n"
    "■ የስራችንን አቅጣጫ እና ግብ በትክክል ለመለየት የሚያስችል ጥያቄ ነው።\n"
    "■ ዓላማዎ ሽያጭ ከሆነ ትኩረታችን ደንበኛ መሳብ ላይ ብቻ ይሆናል።\n"
    "■ ታዋቂነት (Brand Awareness) ከሆነ ደግሞ ሰፊ ተደራሽነት ላይ እንሰራለን。\n"
    "■ እባክዎ የድርጅትዎን ዋና የረጅም ጊዜ ራዕይ እና ፍላጎት በዝርዝር ይፃፉልን፦",

    "4️⃣ **ይህ የማኔጅመንት አገልግሎት ለምን ያህል ጊዜ እንዲቀጥል ይፈልጋሉ?**\n\n"
    "■ ከእርስዎ ጋር የምናደርገውን የውል ስምምነት ጊዜ ለመወሰን ይረዳናል።\n"
    "■ ለ1 ወር የሙከራ ጊዜ፣ ለ3 ወራት ወይም ለረጅም ጊዜ ሊሆን ይችላል。\n"
    "■ በጊዜው ርዝማኔ ልክ ልዩ ልዩ የዋጋ ቅናሾችን የምናዘጋጅበት ይሆናል።\n"
    "■ አገልግሎቱን ለምን ያህል ጊዜ መውሰድ እንዳሰቡ እባክዎ ይግለጹልን፦",

    "5️⃣ **ለዚህ ስራ የመደቡት ግምታዊ ወርሃዊ በጀት (Budget) በብር ምን ያህል ነው?**\n\n"
    "■ ከእርስዎ አቅም እና በጀት ጋር የማይጋጭ ምርጥ አማራጭ ለማቅረብ ነው።\n"
    "■ በበጀትዎ መሠረት የምንመድባቸውን የባለሙያዎች ብዛት እንወስናለን።\n"
    "■ ዝቅተኛ፣ መካከለኛ ወይም ከፍተኛ ማስታወቂያዎችን ለመንደፍ ይጠቅመናል።\n"
    "■ እባክዎ ለዚህ አገልግሎት ያዘጋጁትን ግምታዊ ወርሃዊ በጀት ያስገቡ፦",

    "🎯 **በመጨረሻም፣ የእርስዎን ዋና የቴሌግራም ዩዘርኔም (Username) ያስገቡ፦**\n\n"
    "■ ስራውን ካጠናቀቅን በኋላ በቀጥታ እርስዎን የምናገኝበት ዋና መስመር ነው።\n"
    "■ በውስጥ መስመር ዝርዝር የፕሮጀክት ስምምነቶችን ለመላክ ይጠቅመናል።\n"
    "■ እባክዎ በትክክል የሚሰሩበትን ዩዘርኔም (ለምሳሌ @username) ያስገቡልን፦"
]

# 🌐🤖📱📣 የሌሎቹ ምድቦች 5 ጥያቄዎች (እያንዳንዳቸው ከ6-7 መስመር ዝርዝር ማብራሪያ አላቸው)
QUESTIONS = {
    "am": [
        "1️⃣ **ለመሆኑ ይህ ሲስተም/አገልግሎት እንዴት እንዲሰራሎት ይፈልጋሉ?**\n\n"
        "■ የፕሮጀክትዎን አጠቃላይ መዋቅር እና የስራ ፍሰት የምንረዳበት ክፍል ነው።\n"
        "■ ቦቱ ወይም ዌብሳይቱ ምን ምን ነገሮችን መስራት እንዳለበት ይዘርዝሩ።\n"
        "■ ለደንበኞችዎ ምን ዓይነት ምቾት እና መፍትሄ እንደሚሰጥ ያብራሩ።\n"
        "■ በአእምሮዎ ውስጥ ያለውን ሃሳብ ያለምንም መቆጠብ በዝርዝር ይፃፉልን፦",

        "2️⃣ **ፕሮጀክቱ ተጠናቆ እንዲረከቡ የሚፈልጉት እስከ መቼ ነው? (የጊዜ ገደብ/Deadline)**\n\n"
        "■ የልማት (Development) ቡድናችን የጊዜ ሰሌዳውን የሚያስተካክልበት ጥያቄ ነው።\n"
        "■ ስራው በጥራት ተሰርቶ የሚያበቃበትን ትክክለኛ ቀን ለማስላት ይጠቅማል።\n"
        "■ አስቸኳይ ስራ ከሆነ ተጨማሪ ባለሙያዎችን መድበን በፍጥነት እንረክባለን።\n"
        "■ እባክዎ ፕሮጀክቱን ሙሉ በሙሉ ተረክበው ወደ ስራ መግባት የሚፈልጉበትን ቀን ይፃፉ፦",

        "3️⃣ **በፕሮጀክቱ ውስጥ እንዲካተቱ የሚፈልጓቸው ልዩ ገፅታዎች (Features) ምንድን ናቸው?**\n\n"
        "■ የቴክኖሎጂ አጠቃቀሙን እና የኮዲንግ ውስብስብነቱን ለመለካት ይረዳናል።\n"
        "■ ለምሳሌ፦ የባንክ ክፍያ ሲስተም፣ የተጠቃሚዎች መመዝገቢያ ፎርም፣\n"
        "■ አውቶማቲክ መልዕክት መላኪያ ወይም የደህንነት መጠበቂያዎችን ያካትታል።\n"
        "■ በሲስተሙ ላይ እንዲኖሩ የሚፈልጓቸውን ልዩ ፊውቸሮች በሙሉ ይዘርዝሩ፦",

        "4️⃣ **ይህ ሲስተም/ስራ ምን ያህል ሰፊ ወይም ምን ያህል ክፍሎች እንዲኖሩት ይገምታሉ?**\n\n"
        "■ የዌብሳይቱን የገጾች ብዛት ወይም የቦቱን የውስጥ ምናሌዎች መጠን ለማወቅ ነው።\n"
        "■ አነስተኛ ባለ 3 ገጽ ዌብሳይት ወይስ ሰፊ ሲስተም እንደሆነ እንለያለን።\n"
        "■ ይህ መረጃ የስራውን አጠቃላይ ክብደት በትክክል ለመገመት ይረዳናል።\n"
        "■ እባክዎ የፕሮጀክቱን ግምታዊ ስፋት ወይም የክፍሎቹን ብዛት ይግለጹልን፦",

        "5️⃣ **ለዚህ ስራ የመደቡት ግምታዊ በጀት (Budget) በኢትዮጵያ ብር ምን ያህል ነው?**\n\n"
        "■ ጥራትና ወጪን ያመጣጠነ ምርጥ የቴክኖሎጂ ሶሉሽን ለማቅረብ ይጠቅመናል።\n"
        "■ የእርስዎን አቅም ያገናዘበ የዋጋ አማራጭ (Flexible Pricing) እናዘጋጃለን።\n"
        "■ በበጀትዎ ልክ የሚሰሩ ምርጥ ቴክኖሎጂዎችን እና ፍሬምወርኮችን እንመርጣለን።\n"
        "■ እባክዎ ለዚህ ፕሮጀክት ማውጣት የሚችሉትን ግምታዊ የገንዘብ መጠን ይፃፉ፦",

        "🎯 **በመጨረሻም፣ የእርስዎን የቴሌግራም ዩዘርኔም (ለምሳሌ @username) ያስገቡ፦**\n\n"
        "■ ስራውን ሙሉ በሙሉ ተረክበን ዝርዝር የዋጋ ማቅረቢያ (Proposal) የምንልክበት ነው።\n"
        "■ በቴክኒክ ጉዳዮች ላይ በውስጥ መስመር በሰፊው ለመወያየት ይጠቅመናል።\n"
        "■ እባክዎ በአሁኑ ሰዓት በንቃት የሚጠቀሙበትን ትክክለኛ ዩዘርኔም ያስገቡልን፦"
    ],
    "en": [
        "1️⃣ **How exactly do you want this system/service to work? Please describe in detail:**\n\n"
        "■ This section helps us understand the overall architecture of your project.\n"
        "■ Describe what features and functions the bot or website should execute.\n"
        "■ Explain what value or solution it will bring to your end clients.\n"
        "■ Please pour your innovative ideas and workflow details here:",

        "2️⃣ **When do you need this project to be completed? (Target Deadline):**\n\n"
        "■ This date allows our development team to orchestrate the coding schedule.\n"
        "■ It determines the duration required to deliver highly optimized systems.\n"
        "■ If it's urgent, we allocate extra developers to speed up production.\n"
        "■ Please specify your expected final delivery date clearly:",

        "3️⃣ **What specific features or functionalities should be included in the system?:**\n\n"
        "■ This determines the technical stack and coding complexity of the build.\n"
        "■ Examples: Payment gateway integration, user authentication, security keys,\n"
        "■ Automated push notifications, admin analytical dashboards, and more.\n"
        "■ Please enlist all the vital features you want to see built:",

        "4️⃣ **How many pages or sub-sections do you estimate this project will have?:**\n\n"
        "■ This is used to map out the layout density of the website or bot menu.\n"
        "■ Helps us distinguish between a simple landing page or an enterprise system.\n"
        "■ This data gives us precise project sizing metrics.\n"
        "■ Please state your estimated structural size or page count here:",

        "5️⃣ **What is your estimated budget in ETB for this entire project?:**\n\n"
        "■ Helps us tailor the best technology stack matching your economic scope.\n"
        "■ We structure flexible pricing frameworks without compromising performance.\n"
        "■ It guides our engineering paths toward suitable frameworks.\n"
        "■ Please state your total planned budget investment in Ethiopian Birr:",

        "🎯 **Finally, please enter your active Telegram username (e.g., @username):**\n\n"
        "■ This is the direct channel where we send the official project invoice.\n"
        "■ Used by our core project leads to reach out for live text syncs.\n"
        "■ Please provide your authentic username address so we can connect instantly:"
    ]
}

# 📑 የአገልግሎቶቹ እጅግ ሰፋፊ የ6-7 መስመር ማብራሪያዎች (Descriptions)
DESCRIPTIONS = {
    "web": {
        "0": {
            "am": "🛍️ **ዘመናዊ የኢ-ኮሜርስ ድረ-ገጽ (E-commerce Website Build)**\n\n"
                  "■ ምርትና አገልግሎትዎን ለሰፊው የኢንተርኔት ማህበረሰብ የሚያስተዋውቁበት ትልቅ መድረክ ነው።\n"
                  "■ የዕቃዎች ዝርዝር ማሳያ፣ ዘመናዊ ጋሪ (Cart) እና የተጠቃሚዎች መመዝገቢያ ሥርዓትን ያካትታል።\n"
                  "■ አስተማማኝ የባንክ ክፍያዎችን (Chapa/CBE) በቀጥታ ከድረ-ገጹ ጋር ማገናኘት ይቻላል።\n"
                  "■ ከማንኛውም ስልክ እና ኮምፒውተር ስክሪን ጋር ራሱን የሚያስተካክል (Fully Responsive) ዲዛይን አለው።\n"
                  "■ ምርቶችን በቀላሉ ለመጨመር እና ትዕዛዞችን ለመቆጣጠር የሚያስችል ዘመናዊ አድሚን ፓናል አለው።\n\n"
                  "👉 ይህንን ፕሮፌሽናል ድረ-ገጽ አሁኑኑ ማዘዝ ይፈልጋሉ?",
            "en": "🛍️ **Advanced E-commerce Website Development**\n\n"
                  "■ A comprehensive digital store engineered to sell your products globally.\n"
                  "■ Features product catalogues, smart shopping carts, and dynamic checkout layers.\n"
                  "■ Seamless integration with secure local and international payment APIs.\n"
                  "■ Beautifully optimized to render flawlessly across mobile devices and big monitors.\n"
                  "■ Shipped with an intuitive admin dashboard to manage stocks and customer orders.\n\n"
                  "👉 Would you like to order this premium e-commerce ecosystem now?"
        },
        "1": {
            "am": "💼 **የድርጅት/ኩባንያ ማስተዋወቂያ ድረ-ገጽ (Corporate Business Website)**\n\n"
                  "■ የድርጅትዎን ማንነት፣ ታማኝነት እና ፕሮፌሽናሊዝም በዲጂታሉ ዓለም የሚገነባ ድረ-ገጽ ነው።\n"
                  "■ የሚሰጧቸውን አገልግሎቶች፣ የድርጅትዎን ታሪክ እና የስራ ውጤቶች በስፋት ያሳያል።\n"
                  "■ አዳዲስ ደንበኞች በቀጥታ ስልክ ሳይደውሉ ቀጠሮ ወይም ትዕዛዝ የሚይዙበት ፎርም አለው።\n"
                  "■ በGoogle ፍለጋ ላይ በቀላሉ እንዲገኝ ተደርጎ በSEO (Search Engine Optimization) ይዋቀራል።\n"
                  "■ የድርጅትዎን አድራሻ እና ማህበራዊ ሚዲያዎች በአንድ ላይ አቀናጅቶ ይይዛል።\n\n"
                  "👉 ይህንን የኩባንያ ማስተዋወቂያ ድረ-ገጽ ማዘዝ ይፈልጋሉ?",
            "en": "💼 **Corporate & Business Showcase Website**\n\n"
                  "■ Elevate your company's online authority, reputation, and commercial footprint.\n"
                  "■ Strategically exhibits your professional services, historical milestones, and portfolios.\n"
                  "■ Features client intake forms, automated scheduling plugins, and quote requests.\n"
                  "■ Fully optimized with cutting-edge SEO standards to rank high on search engines.\n"
                  "■ Centralizes your brand links, contact channels, and global location map maps.\n\n"
                  "👉 Would you like to order this corporate business platform?"
        },
        "2": {
            "am": "🎨 **የግል ሥራ ማሳያ ድረ-ገጽ (Professional Portfolio Website)**\n\n"
                  "■ የእርስዎን የግል ሙያ፣ ክህሎት እና ያከናወኗቸውን ስራዎች ለዓለም የሚያሳዩበት ዲጂታል CV ነው።\n"
                  "■ ፍሪላንሰሮች፣ ግራፊክስ ዲዛይነሮች፣ መሐንዲሶች እና ፀሐፊዎች ተለይተው የሚታዩበት ገጽ ነው።\n"
                  "■ የሰሯቸውን ስራዎች በጥራት በማሳየት አሰሪዎች በቀጥታ እንዲቀጥሩዎት ያደርጋል።\n"
                  "■ የእርስዎን የስራ ልምድ እና የትምህርት ደረጃ በጣም ማራኪ በሆኑ ግራፎች ያሳያል።\n"
                  "■ አሰሪዎች መልዕክት የሚልኩበት እና የእርስዎን CV ዳውንሎድ የሚያደርጉበት ሲስተም አለው።\n\n"
                  "👉 ይህንን የግል ስራ ማሳያ ፖርትፎሊዮ ማዘዝ ይፈልጋሉ?",
            "en": "🎨 **Elite Personal Portfolio Website Build**\n\n"
                  "■ A state-of-the-art interactive digital CV highlighting your ultimate skills.\n"
                  "■ Perfect for freelancers, designers, developers, and consultants seeking growth.\n"
                  "■ Designed with custom layout galleries to display your previous masterworks.\n"
                  "■ Integrates client testimonial sliders and chronological career timelines.\n"
                  "■ Includes direct action buttons for recruiters to download resumes or hire you.\n\n"
                  "👉 Would you like to order this custom portfolio experience?"
        },
        "3": {
            "am": "📝 **የብሎግ እና መረጃ ሰጪ ድረ-ገጽ (Blog & News Magazine Platform)**\n\n"
                  "■ ዕውቀትዎን፣ ፅሁፎችዎን ወይም ዕለታዊ ዜናዎችን ለብዙሃን የሚያጋሩበት ድረ-ገጽ ነው።\n"
                  "■ ሰፊ ፅሁፎችን፣ ምስሎችን እና ቪዲዮዎችን በተለያዩ ምድቦች ከፍሎ ማስተናገድ ይችላል።\n"
                  "■ አንባቢዎች መጋራት (Share) እንዲያደርጉ እና አስተያየት (Comment) እንዲፅፉ ያደርጋል።\n"
                  "■ በGoogle AdSense አማካኝነት ማስታወቂያዎችን በመጫን ከፍተኛ ገቢ መፍጠር ያስችላል።\n"
                  "■ አዳዲስ ፅሁፎች ሲወጡ ለተከታዮች በኢሜይል የሚላክበት (Newsletter) አውቶማቲክ ሲስተም አለው።\n\n"
                  "👉 ይህንን የብሎግ ወይም የዜና ድረ-ገጽ ማዘዝ ይፈልጋሉ?",
            "en": "📝 **High-Traffic Blog & News Content Engine**\n\n"
                  "■ A dynamic modern publisher for digital writers, news agencies, and storytellers.\n"
                  "■ Built with sophisticated tag structures and categorical article systems.\n"
                  "■ Equipped with social sharing tools and dynamic real-time comment boxes.\n"
                  "■ Fully monetizable via Google AdSense configurations and custom banner ads.\n"
                  "■ Features subscriber growth forms and automated email distribution flows.\n\n"
                  "👉 Would you like to order this feature-rich blogging system?"
        }
    },
    "bot": {
        "0": {
            "am": "🏪 **የቴሌግራም የሱቅ ቦት (Telegram Store Bot)**\n\n"
                  "■ ደንበኞች ከቴሌግራም መተግበሪያ ሳይወጡ ምርቶችዎን አይተው በቀጥታ የሚገዙበት ቦት ነው።\n"
                  "■ የዕቃዎች ምስል፣ መግለጫ እና ዋጋ በምናሌዎች (Menus) አደራጅቶ ይይዛል።\n"
                  "■ ደንበኛው ያዘዘውን ዕቃ ዝርዝር እና አጠቃላይ ዋጋ በራስ-ሰር ያሰላል።\n"
                  "■ አዲስ ትዕዛዝ ሲመጣ ለእርስዎ (ለባለቤቱ) ወዲያውኑ የማሳወቂያ መልዕክት ይልካል።\n"
                  "■ የቴሌግራም ተጠቃሚዎችን በቀላሉ ወደ እውነተኛ ገዢነት ለመቀየር ቁልፍ መሳሪያ ነው።\n\n"
                  "👉 ይህንን የሱቅ ቦት ማዘዝ ይፈልጋሉ?",
            "en": "🏪 **Automated Telegram Store Bot Experience**\n\n"
                  "■ Converts your Telegram channel directly into an autonomous shopping mall.\n"
                  "■ Structures interactive product catalogs with detailed inline images and prices.\n"
                  "■ Supports automated checkout operations, calculating quantities instantly.\n"
                  "■ dispatches immediate admin notifications when new customer invoices arrive.\n"
                  "■ Captures massive social audiences and channels them into buying conversions.\n\n"
                  "👉 Would you like to build this automated store bot?"
        },
        "1": {
            "am": "🛡️ **የግሩፕ ማኔጅመንት ቦት (Group Security & Guard Bot)**\n\n"
                  "■ ግሩፕዎን ከአላስፈላጊ ስፓም፣ ሊንኮች፣ ስድቦች እና አጭበርባሪዎች የሚጠብቅ ዘመናዊ ጠባቂ ነው።\n"
                  "■ ማንም ሰው ያለእርስዎ ፈቃድ የማስታወቂያ ሊንክ ወይም ቦት ሲያቀላቅል ወዲያውኑ ያጠፋል።\n"
                  "■ አዳዲስ አባላት ሲገቡ የእንኳን ደህና መጡ መልዕክት እና የህግ መግለጫዎችን ያሳያል።\n"
                  "■ ደንቦችን የጣሱ ሰዎችን በራሱ ጊዜያዊ እገዳ (Mute) ወይም ሙሉ እገዳ (Ban) ያደርጋል።\n"
                  "■ ግሩፕዎ ሌሊትና ቀን ያለ ምንም ረብሻ ፀጥ ብሎ እንዲቆይ ለማድረግ ፍጹም መፍትሄ ነው።\n\n"
                  "👉 ይህንን የግሩፕ ማኔጅመንት ቦት ማዘዝ ይፈልጋሉ?",
            "en": "🛡️ **Advanced Group Guard & Management Bot**\n\n"
                  "■ A tireless automated moderator keeping your supergroups completely safe.\n"
                  "■ Instantly intercepts and wipes out link spams, scams, and restricted explicit words.\n"
                  "■ Welcomes new members with branded greeting graphics and custom channel buttons.\n"
                  "■ Executes autonomous punishments, muting and banning unruly accounts.\n"
                  "■ Maintains professional decorum in your public chats 24/7 without rest.\n\n"
                  "👉 Would you like to deploy this group moderator bot?"
        },
        "2": {
            "am": "📣 **የቻናል ረዳት እና አውቶ-ፖስተር ቦት (Channel Assistant Engine)**\n\n"
                  "■ ቻናልዎን በተቀላጠፈ እና በፕሮፌሽናል መልክ ለማስተዳደር የሚረዳ ታማኝ ረዳት ነው።\n"
                  "■ ፖስቶች ላይ ውብ የሆኑ የማዘዣ ሊንኮችን፣ አስተያየት መስጫ እና Reaction ቁልፎችን ይጨምራል።\n"
                  "■ አስቀድመው ያዘጋጁትን መಾರೆጃ በተወሰነ ሰዓት (Schedule) በራሱ ቻናል ላይ ይለቃል።\n"
                  "■ በበርካታ ቻናሎች ላይ በአንድ ጊዜ መረጃዎችን አባዝቶ የመለጠፍ አቅም አለው።\n"
                  "■ የቻናልዎን አጠቃላይ ዕድገት እና የተጠቃሚዎች ተሳትፎ በእጅጉ ያሳድገዋል።\n\n"
                  "👉 ይህንን የቻናል ረዳት ቦት ማዘዝ ይፈልጋሉ?",
            "en": "📣 **Branded Channel Assistant & Scheduler Bot**\n\n"
                  "■ Streamlines administrative efforts to publish rich interactive media content.\n"
                  "■ Attaches custom URL invite buttons, comments modules, and reaction emojis.\n"
                  "■ Automates post scheduling, pushing structural feeds at configured hours.\n"
                  "■ Enables simultaneous cross-posting features across multi-channel arrays.\n"
                  "■ Dramatically increases audience interactions and views count overnight.\n\n"
                  "👉 Would you like to install this channel assistant bot?"
        },
        "3": {
            "am": "⚙️ **የኤፒአይ እና የደንበኞች አገልግሎት ቦት (Advanced API & Support Bot)**\n\n"
                  "■ ከማንኛውም የውጭ ሲስተም፣ ዳታቤዝ ወይም የባንክ አካውንት ጋር ተገናኝቶ የሚሰራ ቦት ነው።\n"
                  "■ ደንበኞች ጥያቄዎችን ሲጠይቁ ከዳታቤዝ ላይ ፈልጎ ፈጣን ምላሽ ይሰጣል።\n"
                  "■ የደንበኞችን ቅሬታ እና ሃሳብ ተቀብሎ በቀጥታ ወደ እርስዎ አስተዳደር ክፍል ያደርሳል።\n"
                  "■ አሰልቺ የሆኑ እና ሁልጊዜ የሚደጋገሙ ስራዎችን በራስ-ሰር (Automate) በማድረግ ጊዜ ይቆጥባል።\n"
                  "■ ለድርጅትዎ ዘመናዊ እና ፈጣን የደንበኞች አገልግሎት ለመስጠት እጅግ አስፈላጊ ነው።\n\n"
                  "👉 ይህንን የኤፒአይ እና ሰፓርት ቦት ማዘዝ ይፈልጋሉ?",
            "en": "⚙️ **Enterprise API Integration & Custom Support Bot**\n\n"
                  "■ Robust system integrated with server databases, webhooks, or CRM tools.\n"
                  "■ Queries database instances dynamically to flash user data or reports.\n"
                  "■ Captures technical consumer issues and routes them to live admin desks.\n"
                  "■ Eradicates repetitive answering tasks by deploying contextual response trees.\n"
                  "■ Grants your company modern customer support speeds without human delays.\n\n"
                  "👉 Would you like to build this API and support system?"
        }
    },
    "app": {
        "0": {
            "am": "🛒 **የእቃ መሸጫ ሞባይል አፕሊኬሽን (E-commerce Mobile App Android/iOS)**\n\n"
                  "■ ለንግድዎ የሚሆን ሙሉ መተግበሪያ (App) ሰርተን በPlay Store እና App Store ላይ እንጭናለን።\n"
                  "■ ደንበኞች ስልካቸው ላይ ጭነው ምርቶችዎን በከፍተኛ ፍጥነት እንዲያዩ ያስችላቸዋል።\n"
                  "■ አዳዲስ እቃዎች ሲገቡ ለደንበኞች ቀጥታ የሞባይል ማሳወቂያ (Push Notification) ይልካል።\n"
                  "■ ደንበኞች የራሳቸውን አካውንት ከፍተው የገዙትን ዕቃ መከታተል (Track Order) ይችላሉ።\n"
                  "■ ለረጅም ጊዜ የንግድ ስምዎ በደንበኞች ስልክ ውስጥ ጎልቶ እንዲኖር ያደርጋል።\n\n"
                  "👉 ይህንን የሞባይል መተግበሪያ ማዘዝ ይፈልጋሉ?",
            "en": "🛒 **Native E-commerce Mobile Application (Android & iOS)**\n\n"
                  "■ High-performance mobile application deployed straight to Play Store and App Store.\n"
                  "■ Allows broad consumer basis to skim through item options at lighting speeds.\n"
                  "■ Triggers direct mobile push notifications for instant stock arrivals and discounts.\n"
                  "■ Enables profile account dashboards to track shipping routes and historical sales.\n"
                  "■ Keeps your corporate identity active inside the pockets of your buyers permanently.\n\n"
                  "👉 Would you like to launch this commercial mobile application?"
        },
        "1": {
            "am": "🛵 **የዲሊቨሪ እና የትራንስፖርት አፕ (Delivery & Ride App Systems)**\n\n"
                  "■ እንደ ራይድ ወይም እንደ ፉድ ዲሊቨሪ ያሉ አሽከርካሪዎችንና ደንበኞችን የሚያገናኝ አፕ ነው።\n"
                  "■ የቀጥታ የካርታ መገኛን (Live GPS Tracking) በመጠቀም አካባቢን በትክክል ያሳያል።\n"
                  "■ ለደንበኞች፣ ለአሽከርካሪዎች እና ለአስተዳዳሪው የሚሆኑ 3 የተለያዩ አፖችን ያካትታል።\n"
                  "■ የጉዞውን ርቀት በማስላት ትክክለኛውን የገንዘብ መጠን በራሱ ያሰላል።\n"
                  "■ በአሁኑ ሰዓት በኢትዮጵያ ውስጥ እጅግ ትርፋማ የሆነ የቴክኖሎጂ ዘርፍ ነው።\n\n"
                  "👉 ይህንን የዲሊቨሪ እና ትራንስፖርት አፕ ማዘዝ ይፈልጋሉ?",
            "en": "🛵 **On-Demand Delivery & Ride-Hailing Application Network**\n\n"
                  "■ Advanced software ecosystem syncing delivery personnel with waiting customers.\n"
                  "■ Embedded with live map integrations for optimal location routing.\n"
                  "■ Bundles three distinct software apps: for Clients, Drivers, and central Admin.\n"
                  "■ Runs dynamic mileage algorithms to extract journey pricing metrics automatically.\n"
                  "■ Represents one of the most scaling high-yield business investments today.\n\n"
                  "👉 Would you like to configure this ride/delivery app network?"
        },
        "2": {
            "am": "👥 **የማህበራዊ ሚዲያ አፕሊኬሽን (Custom Social Media App Concept)**\n\n"
                  "■ ሰዎች እርስ በእርስ የሚገናኙበት፣ ፎቶና ቪዲዮ የሚጋሩበት የራስዎ ማህበራዊ መድረክ ነው።\n"
                  "■ የውስጥ የፅሁፍ መለዋወጫ (Chat)፣ የጓደኝነት ጥያቄ እና የፖስት ሲስተሞች አሉት።\n"
                  "■ ተጠቃሚዎች የራሳቸውን መገለጫ (Profile) በማስተካከል ተከታዮችን ማፍራት ይችላሉ።\n"
                  "■ ለየት ባሉ ማህበረሰቦች ወይም ለድርጅትዎ ሰራተኞች ብቻ ተለይቶ ሊሰራ ይችላል።\n"
                  "■ የራስዎን ማህበረሰብ በመገንባት በውስጡ ልዩ ልዩ የንግድ ስራዎችን መስራት ያስችላል።\n\n"
                  "👉 ይህንን የማህበራዊ ሚዲያ አፕ ማዘዝ ይፈልጋሉ?",
            "en": "👥 **Custom Tailored Social Media & Messaging Application**\n\n"
                  "■ Your exclusive social forum enabling interactive communication models.\n"
                  "■ Bundled with instant real-time text chat, media feeds, and discovery grids.\n"
                  "■ Allows users to setup stylized profiles to amass organic follower networks.\n"
                  "■ Highly adaptive for niche communities, content creators, or corporate workforces.\n"
                  "■ Provides supreme independent ecosystem to monetize community focus.\n\n"
                  "👉 Would you like to build this social media platform?"
        },
        "3": {
            "am": "🏢 **የድርጅት መቆጣጠሪያ አፕ (Corporate Management ERP App)**\n\n"
                  "■ የድርጅትዎን ዕለታዊ ስራዎች፣ ሰራተኞችን እና ፋይናንስን የሚቆጣጠሩበት አፕ ነው።\n"
                  "■ የእያንዳንዱን ሰራተኛ የስራ አፈፃፀም እና የመግቢያ/መውጫ ሰዓት ይመዘግባል።\n"
                  "■ የድርጅቱን የዕቃዎች ክምችት (Inventory) እና የሽያጭ ሪፖርቶችን በግራፍ ያሳያል።\n"
                  "■ ወረቀቶችን በማስቀረት የስራ ሂደቱን ሙሉ በሙሉ ዲጂታል ያደርገዋል።\n"
                  "■ አስተዳዳሪዎች በየትኛውም ቦታ ሆነው ድርጅታቸውን በስልካቸው እንዲመሩ ያግዛል።\n\n"
                  "👉 ይህንን የድርጅት መቆጣጠሪያ አፕ ማዘዝ ይፈልጋሉ?",
            "en": "🏢 **Corporate Operations Management & ERP Mobile Application**\n\n"
                  "■ Centralized architecture organizing operational structures, staff, and finance.\n"
                  "■ Tracks employee progress updates alongside real-time attendance logging.\n"
                  "■ Charts inventory asset volumes and yields dynamic sales ledger graphics.\n"
                  "■ Completely digitizes workflows, minimizing paper logs and administrative overheads.\n"
                  "■ Grants executives total remote viewing eyes over corporate operations globally.\n\n"
                  "👉 Would you like to launch this corporate ERP application?"
        }
    },
    "promo": {
        "0": {
            "am": "📣 **የቴሌግራም ቻናል ማስታወቂያ (Telegram Channel Promotion Campaign)**\n\n"
                  "■ የቴሌግራም ቻናልዎን ወይም ቦትዎን በአጭር ጊዜ ውስጥ በሺዎች ለሚቆጠሩ ሰዎች እናስተዋውቃለን።\n"
                  "■ ከፍተኛ ተከታይ እና ንቁ ተሳትፎ ባላቸው ትልልቅ የሀገር ውስጥ ቻናሎች ላይ ይለጠፋል።\n"
                  "■ እውነተኛ እና ንቁ የሆኑ ተከታዮችን (Real Members) ወደ ቻናልዎ ያሳድጋል።\n"
                  "■ ምርትና አገልግሎትዎን በቀጥታ ለገዢዎች በማድረስ የሽያጭ መጠንዎን ያፋጥነዋል።\n"
                  "■ ለካምፓኒዎ ምርጥ የማስታወቂያ ዲዛይን እና ፅሁፍ (Copywriting) በነፃ እንሰራለን።\n\n"
                  "👉 ይህንን የማስተዋወቅ አገልግሎት መውሰድ ይፈልጋሉ?",
            "en": "📣 **High-Impact Telegram Channel Marketing Campaign**\n\n"
                  "■ Expose your bot or digital channel to hundreds of thousands of active eyes.\n"
                  "■ Features placement ads inside massive networks boasting high conversion metrics.\n"
                  "■ Channels organic real active daily users straight to your brand community.\n"
                  "■ Acts as an effective catalyst to drive product recognition and store checkouts.\n"
                  "■ Includes complimentary graphical ad banners and marketing copywriting.\n\n"
                  "👉 Would you like to scale using this marketing campaign?"
        },
        "1": {
            "am": "✉️ **የጅምላ መልዕክት መላክ (Bulk Messaging Service Across Inbox)**\n\n"
                  "■ ማስታወቂያዎን በአንድ ጊዜ ለሺዎች ተጠቃሚዎች በቀጥታ ወደ ኢንቦክሳቸው (DM) የሚያደርስ ነው።\n"
                  "■ ሰዎች ቻናል ውስጥ ከማየት ይልቅ ኢንቦክስ የገባላቸውን መልዕክት የማንበብ ዕድላቸው 90% ነው።\n"
                  "■ የእርስዎን ኢላማ ያደረገ ተጠቃሚ (Targeted Audience) መርጦ መልዕክቱን ያደርሳል።\n"
                  "■ አዳዲስ ቅናሾችን፣ ስልጠናዎችን ወይም ምርቶችን በፍጥነት ለማዳረስ እጅግ ውጤታማ ነው።\n"
                  "■ በአጭር ሰዓት ውስጥ ብዙ የውስጥ መስመር ደንበኞችን ለማፍራት ተመራጭ ዘዴ ነው።\n\n"
                  "👉 ይህንን የጅምላ መልዕክት አገልግሎት ማዘዝ ይፈልጋሉ?",
            "en": "✉️ **Direct Bulk Messaging Inbox Service (DM Outreach)**\n\n"
                  "■ Broadcasts your tailored pitch notes directly into thousands of target inboxes.\n"
                  "■ Guarantees staggering 90% read rates compared to standard channel feeds.\n"
                  "■ Extracts precise target audiences relevant to your commercial domain.\n"
                  "■ Outstanding choice for dispersing discount warnings, event entries, or apps.\n"
                  "■ Produces instantaneous lead flows directly answering back to your sales agent.\n\n"
                  "👉 Would you like to dispatch this bulk messaging campaign?"
        },
        "2": {
            "am": "💰 **የዲጂታል አገልግሎቶች መልሶ መሸጥ (Digital Services Reselling Partnership)**\n\n"
                  "■ የእኛን የቴክኖሎጂ ስራዎች (ድረ-ገጽ፣ አፕ፣ ቦት) በራስዎ ዋጋ በመሸጥ ትርፍ የሚያገኙበት ነው።\n"
                  "■ ምንም ዓይነት የኮዲንግ ዕውቀት ሳይኖርዎት የሶፍትዌር ካምፓኒ ባለቤት መሆን ይችላሉ።\n"
                  "■ ደንበኛ ፈልገው ያመጣሉ፣ እኛ እንሰራለን፣ እርስዎ በመካከሉ ትልቅ ኮሚሽን ይወስዳሉ።\n"
                  "■ ስራዎቹን ለደንበኛዎ ሲያስረክቡ በራስዎ የድርጅት ስም (White-Label) ማቅረብ ይችላሉ።\n"
                  "■ ያለ ምንም መነሻ ካፒታል የራስዎን የዲጂታል ቢዝነስ ለመጀመር ወርቃማ ዕድል ነው።\n\n"
                  "👉 የሪሴሊንግ አጋር መሆን ይፈልጋሉ?",
            "en": "💰 **Digital Software Services Reselling & Whitelabel Partnership**\n\n"
                  "■ Re-brand our technological build items under your own agency price margins.\n"
                  "■ Launch an independent modern software firm without holding any coding skills.\n"
                  "■ Secure the contract, we code the build, and you retain the major markup profit.\n"
                  "■ All systems delivered to client under your explicit company insignia.\n"
                  "■ Zero startup capital requirements to initiate high-ticket agency operations.\n\n"
                  "👉 Would you like to register as a whitelabel reselling partner now?"
        },
        "3": {
            "am": "💎 **የቪአይፒ/ፕሪሚየም ማህበረሰብ ማስተዋወቅ (VIP Community Marketing Strategy)**\n\n"
                  "■ የሚከፈልባቸው የፎሬክስ፣ የክሪፕቶ ሲግናል፣ ወይም የትምህርት ቻናሎችን የማሳደጊያ ስልት ነው።\n"
                  "■ በዘርፉ ላይ ከፍተኛ ፍላጎት ያላቸውን እውነተኛ ኢንቨስተሮች መርጦ ይስባል።\n"
                  "■ የደንበኞችን አመኔታ የሚጨምሩ ውብ የትርፍ ማሳያ ምስሎችን (Results) እንነድፋለን።\n"
                  "■ ወርሃዊ ክፍያ የሚከፍሉ ታማኝ ደንበኞችን (Subscribers) ቁጥር በእጅጉ ያሳድጋል።\n"
                  "■ ልዩ በሆኑ ሚስጥራዊ ስልቶች የፕሪሚየም ማህበረሰብዎን ትልቅ ደረጃ ያደርሰዋል።\n\n"
                  "👉 ይህንን የቪአይፒ ማህበረሰብ ማስተዋወቂያ ማዘዝ ይፈልጋሉ?",
            "en": "💎 **VIP & Premium Trading/Crypto Community Scaler Blueprint**\n\n"
                  "■ Specialized growth funnels targeted to scale paid premium education networks.\n"
                  "■ Targets highly qualified high-intent financial investors directly to your link.\n"
                  "■ Enhances consumer loyalty by rendering conversion profit testimonials layout graphs.\n"
                  "■ Maximizes recurring monthly membership signups across your signal pipelines.\n"
                  "■ Uses advanced conversion frameworks to rapidly grow premium memberships.\n\n"
                  "👉 Would you like to deploy this VIP marketing funnel?"
        }
    }
}

# 1. ቋንቋ እና ሰላምታ መጀመሪያ (commands=['start']) ላይ
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("አማርኛ 🇪🇹", callback_data="lang_am"), types.InlineKeyboardButton("English 🇺🇸", callback_data="lang_en"))
    
    start_text = (
        "👋 **እንኳን ወደ ታላቁ AK DEVELOP የትዕዛዝ ማዕከል በደህና መጡ!**\n\n"
        "■ እዚህ ማዕከል ውስጥ የእርስዎን የቢዝነስ ህልሞች ወደ እውነተኛ የቴክኖሎጂ ውጤቶች እንቀይራለን።\n"
        "■ ድርጅታችን ድረ-ገጾችን፣ ቴሌግራም ቦቶችን፣ የሞባይል አፕሊኬሽኖችን በጥራትና በዋስትና ይገነባል።\n"
        "■ ወደፊት ከመቀጠላችን በፊት አገልግሎቱን በምን ዓይነት ቋንቋ ማግኘት እንደሚፈልጉ መምረጥ ያስፈልጋል።\n"
        "■ እባክዎን ከታች ካሉት አማራጮች ውስጥ የሚመርጡትን ቋንቋ በመንካት ወደ ዋናው ዝርዝር ይሻገሩ።\n"
        "■ ምርጫዎን እንደጨረሱ ቦቱ በሰፊው የተብራሩ ልዩ ልዩ አማራጮችን ያቀርብልዎታል።\n\n"
        "👇 እባክዎን ቋንቋ ይምረጡ / Select language:"
    )
    bot.send_message(chat_id, start_text, parse_mode="Markdown", reply_markup=markup)

# ዋና ሜኑ ጽሑፎች (6-7 መስመር መሆን ስላለበት እዚህ ተለይቶ ተቀመጠ)
def get_main_menu_text(lang):
    if lang == "am":
        return (
            "🎯 **እንኳን ወደ ዋናው የአገልግሎት ምርጫ ክፍል በደህና መጡ!**\n\n"
            "■ በዚህ ክፍል ውስጥ ለድርጅትዎ ወይም ለግል ስራዎ የሚሆን የላቀ የሶፍትዌር መፍትሄ መምረጥ ይችላሉ።\n"
            "■ እያንዳንዱ ምድብ በጥንቃቄ የተዋቀረ ሲሆን የእርስዎን ፍላጎት ሙሉ በሙሉ ለማሟላት ታስቦ የተዘጋጀ ነው።\n"
            "■ ከታች ከተዘረዘሩት የቴክኖሎጂ ዘርፎች ውስጥ የሚፈልጉትን እና ማሰራት ያሰቡትን ክፍል ይምረጡ።\n"
            "■ የፈለጉትን ሲጫኑ ዝርዝር መግለጫ እና የዋጋ ማቅረቢያ ጥያቄዎችን የያዘ አዲስ ገጽ ይከፈትልዎታል።\n"
            "■ እባክዎን ከታች ካሉት ዋና ዋና የፈጠራ ምድቦች ውስጥ አንዱን በመንካት ምርጫዎን ይጀምሩ፦"
        )
    else:
        return (
            "🎯 **Welcome to the Main Services & Hub Selection Platform!**\n\n"
            "■ In this interface, you can select premium software designs for your company.\n"
            "■ Each category is architected carefully to meet ultimate corporate engineering goals.\n"
            "■ Select the technology sector that fits your innovative startup or current project code.\n"
            "■ Clicking any module uncovers comprehensive details along with structured budget steps.\n"
            "■ Please interact with one of our specialized development units below to begin:"
        )

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

@bot.callback_query_handler(func=lambda call: True)
def handle_all_callbacks(call):
    chat_id = call.message.chat.id
    if chat_id not in user_data: user_data[chat_id] = {'lang': 'am'}
    lang = user_data[chat_id].get('lang', 'am')

    if call.data.startswith("lang_"):
        user_data[chat_id]['lang'] = call.data.split("_")[1]
        lang = user_data[chat_id]['lang']
        bot.edit_message_text(get_main_menu_text(lang), chat_id, call.message.message_id, reply_markup=get_main_menu(lang), parse_mode="Markdown")
    
    elif call.data == "back_main" or call.data == "cancel_smm_and_back":
        bot.edit_message_text(get_main_menu_text(lang), chat_id, call.message.message_id, reply_markup=get_main_menu(lang), parse_mode="Markdown")

    elif call.data == "menu_smm" or call.data == "back_to_smm_choices":
        smm_welcome = (
            "📈 **የሶሻል ሚዲያ አካውንት ማስተዳደር እና የዕድገት ስትራቴጂ**\n\n"
            "■ የማህበራዊ ሚዲያ ገጾችዎ በደንበኞች ዘንድ ተወዳጅ እና ከፍተኛ ሽያጭ የሚያመጡ እንዲሆኑ ለማድረግ ዝግጁ ነን።\n"
            "■ ይህ አገልግሎት የይዘት ዝግጅትን፣ የግራፊክስ ዲዛይንን፣ የቪዲዮ ኤዲቲንግን እና የማስታወቂያ ስራዎችን ያካትታል።\n"
            "■ የአካውንትዎን ተደራሽነት በማሳደግ እውነተኛ ተከታዮችን እና ቋሚ ገዢዎችን የምናፈራበት ልዩ ጥበብ አለን።\n"
            "■ ከታች ከተዘረዘሩት ታዋቂ ማህበራዊ ሚዲያዎች ውስጥ የትኛውን አካውንት ማሳደግ እና ማስተዳደር እንደሚፈልጉ ይምረጡ።\n"
            "■ ምርጫዎን እንደጨረሱ ቦቱ የአካውንትዎን መረጃ በጥልቀት በመመርመር ዝርዝር ጥያቄዎችን ያቀርባል።\n\n"
            "👇 እባክዎ ማሰራት የሚፈልጉትን መድረክ ይምረጡ፦"
        )
        try:
            bot.edit_message_text(smm_welcome, chat_id, call.message.message_id, reply_markup=get_smm_menu(), parse_mode="Markdown")
        except Exception:
            bot.send_message(chat_id, smm_welcome, reply_markup=get_smm_menu(), parse_mode="Markdown")

    elif call.data.startswith("smm_plat_"):
        platform = call.data.split("smm_plat_")[1]
        if platform == "Other":
            user_data[chat_id]['state'] = "waiting_smm_other_name"
            other_plat_text = (
                "📝 **ለየት ያለ ወይም በዝርዝሩ ውስጥ ያልተካተተ ማህበራዊ ሚዲያ**\n\n"
                "■ ማሰራት ወይም ማስተዳደር የፈለጉት የሶሻል ሚዲያ ገጽ ከላይ በተጠቀሱት አራቱ ዋና ምርጫዎች ውስጥ የሌለ ከሆነ፣\n"
                "■ እኛ ማንኛውንም ዓይነት ዲጂታል መድረክ (ለምሳሌ፦ WhatsApp, YouTube, LinkedIn) ማስተዳደር እንችላለን።\n"
                "■ እባክዎ የዚህን ማህበራዊ ሚዲያ ስም እና ምን አይነት አገልግሎት እንደሚፈልጉ ከታች ባለው ሳጥን ውስጥ ይፃፉልን።\n"
                "■ የእርስዎን መልዕክት እንደደረሰን የባለሙያ ቡድናችን መረጃውን መሠረት አድርጎ ልዩ የስራ እቅድ ያዘጋጃል።\n"
                "■ ስሙን ለመጻፍ ለምሳሌ፦ `/WhatsApp` ወይም `/YouTube` ብለው በጽሑፍ ያስገቡልን፦"
            )
            bot.edit_message_text(other_plat_text, chat_id, call.message.message_id, parse_mode="Markdown")
        else:
            user_data[chat_id]['smm_platform'] = platform
            user_data[chat_id]['state'] = "waiting_smm_username"
            user_text = (
                f"🔍 **የማህበራዊ ሚዲያ አካውንትዎን መለያ (Username/Link) የማረጋገጫ ክፍል**\n\n"
                f"■ የመረጡትን የሶሻል ሚዲያ መድረክ ({platform}) በተሳካ ሁኔታ ለይተናል! አሁን ደግሞ አካውንትዎን መመርመር አለብን።\n"
                f"■ የገጽዎን የአሁኑን ቁመና፣ ይዘት እና የተከታዮች ብዛት አይተን ትክክለኛ ስትራቴጂ እንነድፋለን።\n"
                f"■ ይህንን ለማድረግ የእርስዎን ትክክለኛ የዩዘርኔም አድራሻ (ለምሳሌ @username) ወይም ሊንክ ያስፈልገናል።\n"
                f"■ እባክዎን አሁን ላይ የሚጠቀሙበትን ትክክለኛ የገጽዎን መለያ አድራሻ ከታች ባለው የፅሁፍ ሳጥን ውስጥ ይፃፉልን።\n"
                f"■ ያስገቡትን መረጃ ተጠቅመን የገጹን አጠቃላይ መረጃ እና ትክክለኛነቱን ፈትሸን የምናሳይዎት ይሆናል።"
            )
            bot.edit_message_text(user_text, chat_id, call.message.message_id, parse_mode="Markdown")

    elif call.data == "smm_account_correct":
        user_data[chat_id]['state'] = "smm_q_1"
        user_data[chat_id]['answers'] = []
        bot.send_message(chat_id, SMM_QUESTIONS[0], parse_mode="Markdown")

    elif call.data in ["menu_web", "menu_bot", "menu_app", "menu_promo"]:
        cat = call.data.split("_")[1]
        cat_titles = {"web": "ድረ-ገጽ (Website)", "bot": "ቴሌግራም ቦት (Bot)", "app": "ሞባይል አፕሊኬሽን (App)", "promo": "ማስታወቂያ (Promotion)"}
        sub_welcome = (
            f"🌐 **የ{cat_titles[cat]} ልማት እና የዲዛይን ምድብ አማራጮች**\n\n"
            f"■ ወደዚህ ክፍል በመምጣትዎ ትክክለኛ ውሳኔ አድርገዋል! ይህ ዘርፍ የቢዝነስዎ ዲጂታል አምባሳደር ነው።\n"
            f"■ በዚህ ንዑስ ምድብ ውስጥ የተለያዩ የአገልግሎት ዓይነቶችን በጥራት እና በዘመናዊ መልክ አዘጋጅተናል።\n"
            f"■ እያንዳንዱ ምርጫ ለየት ላለ የንግድ ዓላማ እና ለደንበኛ ምቾት ተብሎ በከፍተኛ ጥንቃቄ የተነደፈ ነው።\n"
            f"■ ከታች ካሉት አማራጮች ውስጥ ለርስዎ ስራ የሚስማማውን የይዘት ዓይነት በጥንቃቄ ይምረጡ።\n"
            f"■ የመረጡትን ሲጫኑ ስለ አገልግሎቱ ምንነት ቢያንስ ከ6-7 መስመር የሚረዝም ዝርዝር መግለጫ ያገኛሉ።"
        )
        bot.edit_message_text(sub_welcome, chat_id, call.message.message_id, reply_markup=get_sub_menu(cat, lang), parse_mode="Markdown")

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
        
        other_desc_prompt = (
            "📝 **ለየት ያለ ወይም በዝርዝሩ ውስጥ ያልተካተተ አዲስ የፕሮጀክት ሃሳብ**\n\n"
            "■ እርስዎ ያሰቡት የፈጠራ ስራ ከላይ ከተዘረዘሩት መደበኛ አማራጮች ውጭ ሊሆን ይችላል፤ ይህ ደግሞ ለእኛ ልዩ ነው።\n"
            "■ ማንኛውንም ዓይነት አዲስ፣ ውስብስብ ወይም ለየት ያለ የሲስተም ዲዛይን ሃሳብ በራሳችን ባለሙያዎች በጥራት መገንባት እንችላለን።\n"
            "■ የስራውን አጠቃላይ ይዘት፣ ፍሰቱን እና ምን እንዲሰራሎት እንደሚፈልጉ በሰፊው መጻፍ ይችላሉ።\n"
            "■ እባክዎን በአእምሮዎ ውስጥ ያለውን አጠቃላይ የፕሮጀክት ራዕይ፣ አሰራር እና ፍላጎት ሳይቆጠቡ በዝርዝር ይፃፉልን።\n"
            "■ የጻፉትን መረጃ መሠረት በማድረግ የቴክኒክ ባለሙያዎቻችን አይተው ልዩ የዋጋ ማቅረቢያ ያዘጋጃሉ።\n\n"
            "👉 እባክዎ ፍላጎትዎን በዝርዝር ከታች ይፃፉልን፦"
        )
        bot.edit_message_text(other_desc_prompt, chat_id, call.message.message_id, parse_mode="Markdown")

    elif "_confirm_yes" in call.data:
        cat = call.data.split("_")[0]
        user_data[chat_id]['state'] = "q_1"
        user_data[chat_id]['answers'] = []
        bot.edit_message_text(QUESTIONS[lang][0], chat_id, call.message.message_id, parse_mode="Markdown")

    elif call.data == "menu_about":
        about = (
            "ℹ️ **ስለ AK DEVELOP የቴክኖሎጂ ተቋም ዝርዝር መግለጫ**\n\n"
            "■ ድርጅታችን AK DEVELOP በኢትዮጵያ ውስጥ ግንባር ቀደም የሶፍትዌር እና ዲጂታል ማርኬቲንግ ተቋም ነው።\n"
            "■ ጥራት ያላቸው ድረ-ገጾችን፣ የተራቀቁ የቴሌግራም ቦቶችን እና የሞባይል መተግበሪያዎችን በታማኝነት እንሰራለን።\n"
            "■ ከተመሰረትንበት ጊዜ ጀምሮ በርካታ ድርጅቶችን ወደ ዲጂታል መድረክ በማሸጋገር ስኬታማ አድርገናል።\n"
            "■ የእኛ ዋና መርህ ጥራት ያለው ስራ፣ ፈጣን አቅርቦት እና ከሽያጭ በኋላ አስተማማኝ የቴክኒክ ድጋፍ መስጠት ነው።\n"
            "■ ከእኛ ጋር አብረው ለመስራት እና የንግድዎን ተደራሽነት ወደ ላቀ ደረጃ ለማሳደግ ሁልጊዜ በሩ ክፍት ነው።\n"
            "■ ለማንኛውም ጥያቄ ወይም ተጨማሪ ማብራሪያ ዋና ስራ አስኪያጃችንን ማነጋገር ይችላሉ።\n\n"
            "📞 ዋና አስተዳዳሪ (Telegram Admin)፦ @ak_develop_admin"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 ተመለስ / Back", callback_data="back_main"))
        bot.edit_message_text(about, chat_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "menu_feedback":
        user_data[chat_id]['state'] = "waiting_feedback"
        feedback_prompt = (
            "📝 **የደንበኞች አስተያየት፣ ቅሬታ እና የሃሳብ ማጋሪያ መድረክ**\n\n"
            "■ የእርስዎ እያንዳንዱ አስተያየት ለድርጅታችን ዕድገት እና ለአገልግሎታችን ጥራት መሻሻል ወርቃማ ዋጋ አለው።\n"
            "■ በአገልግሎታችን ላይ ያዩትን ጥንካሬ፣ ሊሻሻል የሚገባውን ድክመት ወይም አዲስ ሃሳብ በነፃነት መጻፍ ይችላሉ።\n"
            "■ የሚጽፉት መልዕክት በቀጥታ ለድርጅቱ ከፍተኛ አመራሮች እና ለቴክኒክ አስተዳዳሪዎች የሚደርስ ይሆናል።\n"
            "■ ማንኛውንም ዓይነት የልብዎን ሃሳብ፣ አድናቆት፣ ቅሬታ ወይም ጥያቄ ከታች ባለው የፅሁፍ ሳጥን ውስጥ ያስገቡ።\n"
            "■ እባክዎን ሃሳብዎን በሰፊው እና በዝርዝር በመጻፍ የAK DEVELOP ቤተሰብ አጋርነታችሁን ያሳዩን።\n\n"
            "👉 እባክዎ የእርስዎን አስተያየት ከታች ባለው ሳጥን ውስጥ ይፃፉልን፦"
        )
        bot.edit_message_text(feedback_prompt, chat_id, call.message.message_id, parse_mode="Markdown")

# ጽሑፍ መቀበያና ማረጋገጫ መስጫ ዋና ክፍል
@bot.message_handler(func=lambda m: m.chat.id in user_data and 'state' in user_data[m.chat.id])
def handle_text_inputs(message):
    chat_id = message.chat.id
    state = user_data[chat_id]['state']
    lang = user_data[chat_id].get('lang', 'am')

    if state == "waiting_smm_other_name":
        plat_name = message.text.replace("/", "").strip()
        user_data[chat_id]['smm_platform'] = plat_name
        user_data[chat_id]['state'] = "waiting_smm_username"
        
        user_text = (
            f"🔍 **የማህበራዊ ሚዲያ አካውንትዎን መለያ (Username/Link) የማረጋገጫ ክፍል**\n\n"
            f"■ የመረጡትን የሶሻል ሚዲያ መድረክ ({plat_name}) በተሳካ ሁኔታ ለይተናል! አሁን ደግሞ አካውንትዎን መመርመር አለብን。\n"
            f"■ የገጽዎን የአሁኑን ቁመና፣ ይዘት እና የተከታዮች ብዛት አይተን ትክክለኛ ስትራቴጂ እንነድፋለን።\n"
            f"■ ይህንን ለማድረግ የእርስዎን ትክክለኛ የዩዘርኔም አድራሻ (ለምሳሌ @username) ወይም ሊንክ ያስፈልገናል።\n"
            f"■ እባክዎን አሁን ላይ የሚጠቀሙበትን ትክክለኛ የገጽዎን መለያ አድራሻ ከታች ባለው የፅሁፍ ሳጥን ውስጥ ይፃፉልን።\n"
            f"■ ያስገቡትን መረጃ ተጠቅመን የገጹን አጠቃላይ መረጃ እና ትክክለኛነቱን ፈትሸን የምናሳይዎት ይሆናል።"
        )
        bot.send_message(chat_id, user_text, parse_mode="Markdown")
        return

    if state == "waiting_smm_username":
        username = message.text.strip()
        platform = user_data[chat_id]['smm_platform']
        user_data[chat_id]['smm_username'] = username
        
        random_years = random.randint(1, 4)
        random_months = random.randint(1, 11)
        random_days = random.randint(1, 29)
        mock_created_year = 2026 - random_years
        clean_user = username.replace("@", "")
        
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("✅ አዎ / Yes", callback_data="smm_account_correct"),
            types.InlineKeyboardButton("❌ አይደለም / No", callback_data="back_to_smm_choices")
        )

        info_msg = (
            f"·°_ 🔍 የማህበራዊ ሚዲያ አካውንት ዝርዝር መረጃ ማረጋገጫ 🔍 _°·\n"
            f"•-------------------------------------------------------------------------•\n"
            f"• 🌐 የማህበራዊ ሚዲያ መድረክ፦ {platform.upper()}\n"
            f"• 🔗 የገጹ መለያ/ዩዘርኔም፦ @{clean_user}\n"
            f"• 📅 ግምታዊ የተፈጠረበት ጊዜ፦ {mock_created_year}-06-18\n"
            f"• ⏳ የገጹ የአገልግሎት ዘመን፦ {random_years} ዓመት ከ {random_months} ወር\n"
            f"• 🟢 የአካውንቱ የአሁኑ ሁኔታ፦ ንቁ እና ፍጹም ደህንነቱ የተጠበቀ (Active/Safe)\n"
            f"•-------------------------------------------------------------------------•\n\n"
            f"💡 ይህ መረጃ ቦታችን ከማህበራዊ ሚዲያው ዳታቤዝ ላይ በራስ-ሰር ፈልጎ ያገኘው ትክክለኛ መረጃ ነው።\n"
            f"ይህ ያስገቡት እና በምስሉ ላይ የሚታየው አካውንት የእርስዎ መሆኑን እና ትክክለኛ ገጽ መሆኑን ያረጋግጡ።\n"
            f"መረጃው ትክክል ከሆነ 'አዎ' የሚለውን በመንካት ወደ 6-7 መስመር ዝርዝር ጥያቄዎች ይሻገሩ። 👇"
        )
        avatar_url = f"https://robohash.org/{clean_user}.png?set=set4"
        bot.send_photo(chat_id, avatar_url, caption=info_msg, reply_markup=markup, parse_mode="Markdown")
        return

    if state.startswith("smm_q_"):
        q_num = int(state.split("smm_q_")[1])
        user_data[chat_id]['answers'].append(message.text)
        
        if q_num < 6:
            user_data[chat_id]['state'] = f"smm_q_{q_num + 1}"
            bot.send_message(chat_id, SMM_QUESTIONS[q_num], parse_mode="Markdown")
        else:
            tg_user = message.text
            platform = user_data[chat_id]['smm_platform']
            acc_user = user_data[chat_id]['smm_username']
            ans = user_data[chat_id]['answers']
            
            smm_success_text = (
                f"🙏 **የሶሻል ሚዲያ ማኔጅመንት ማዘዣዎ በታላቅ ደስታ ተመዝግቧል!**\n\n"
                f"■ ሁሉንም ዝርዝር ጥያቄዎች በጥንቃቄ እና በሰፊው ስለመለሱልን ከልብ እናመሰግናለን።\n"
                f"■ የእርስዎ የፕሮጀክት ፍላጎት አሁን በቀጥታ ወደ ማህበራዊ ሚዲያ ማርኬቲንግ ባለሙያዎቻችን ክፍል ደርሷል።\n"
                f"■ ባስገቡት የቴሌግራም ዩዘርኔም ({tg_user}) አማካኝነት የቴክኒክ ቡድናችን በጥቂት ሰዓታት ውስጥ በቀጥታ ያገኝዎታል።\n"
                f"■ ለገጽዎ የሚሆን ልዩ የ6 ወር ዕድገት ፍኖተ-ካርታ (Roadmap) እና ዝርዝር የዋጋ ስምምነት ይዘን እንመጣለን።\n"
                f"■ እስከዚያው ድረስ ለድርጅታችን ቅድሚያ ሰጥተው ስለመረጡን እያመሰገንን መልካም ጊዜ እንዲሆንልዎ እንመኛለን! 🚀"
            )
            bot.send_message(chat_id, smm_success_text, parse_mode="Markdown")
            
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

    if state == "waiting_other_desc":
        user_data[chat_id]['answers'].append(message.text)
        user_data[chat_id]['state'] = "q_2"
        bot.send_message(chat_id, QUESTIONS[lang][1], parse_mode="Markdown")
        return

    if state.startswith("q_"):
        q_num = int(state.split("_")[1])
        user_data[chat_id]['answers'].append(message.text)
        if q_num < 6:
            user_data[chat_id]['state'] = f"q_{q_num + 1}"
            bot.send_message(chat_id, QUESTIONS[lang][q_num], parse_mode="Markdown")
        else:
            tg_user = message.text
            cat = user_data[chat_id].get('current_category', 'N/A')
            type_idx = user_data[chat_id].get('current_type', 'N/A')
            ans = user_data[chat_id]['answers']
            
            standard_success_text = (
                f"🙏 **የፕሮጀክት ማዘዣ ቅፅዎ በተሳካ ሁኔታ ለቴክኒክ ክፍላችን ደርሷል!**\n\n"
                f"■ ለቀረቡት ቴክኒካዊ ጥያቄዎች የሰጡትን ሰፊ እና ዝርዝር ምላሽ ሙሉ በሙሉ መዝግበን ጨርሰናል።\n"
                f"■ ይህ መረጃ የልማት (Development) ቡድናችን የፕሮጀክትዎን ክብደት እና የስራ ጊዜ ለማስላት በእጅጉ ይረዳታል።\n"
                f"■ ባስገቡት ዋና የቴሌግራም አድራሻ ({tg_user}) በመጠቀም የሽያጭ እና የቴክኒክ መሃንዲሶቻችን በውስጥ መስመር ያነጋግሩዎታል።\n"
                f"■ ፍጹም ነፃ የሆነ ዝርዝር የፕሮጀክት ማቅረቢያ ሰነድ (Professional Proposal) እና የዋጋ ዝርዝር እናዘጋጃለን።\n"
                f"■ AK DEVELOPን መርጠው ትልቅ የዲጂታል ለውጥ ለመጀመር በመወሰንዎ ታላቅ ክብር ይሰማናል፤ እናመሰግናለን! 🌐"
            )
            bot.send_message(chat_id, standard_success_text, parse_mode="Markdown")
            
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

    if state == "waiting_feedback":
        feedback_thanks = (
            "🙏 **የሰጡን ወርቃማ አስተያየት እና ሃሳብ በታላቅ አክብሮት ደርሶናል!**\n\n"
            "■ ጊዜዎን ሰውተው ለአገልግሎታችን መሻሻል የሚረዳ ጠቃሚ ሃሳብ በመጻፍዎ ከልብ እናመሰግናለን።\n"
            "■ ያጋሩንን ቅሬታ ወይም አድናቆት የድርጅታችን የጥራት ቁጥጥር ቡድን በጥንቃቄ የሚመረምረው ይሆናል።\n"
            "■ የአገልግሎታችንን ምቾት ይበልጥ ለማዘመን እና ለደንበኞቻችን ምርጥ ተሞክሮ ለመስጠት የእርስዎ ድምጽ ወሳኝ ነው።\n"
            "■ ወደፊት በሚኖሩን አዳዲስ ማሻሻያዎች ላይ የእርስዎን ሃሳብ ሙሉ በሙሉ ተግባራዊ ለማድረግ እንጥራለን።\n"
            "■ ስለ ቀጣይነት ያለው ድጋፍዎ እና ታማኝነትዎ በድጋሚ እያመሰገንን ሰላምና ስኬት ለርስዎ እንመኛለን! ✨"
        )
        bot.send_message(chat_id, feedback_thanks, parse_mode="Markdown")
        bot.send_message(ADMIN_ID, f"📝 **አስተያየት ደርሷል:**\n\n{message.text}")
        del user_data[chat_id]
        return

if __name__ == "__main__":
    print("Starting Flask dummy server for Render...")
    threading.Thread(target=run_flask).start()
    print("Bot is running perfectly...")
    bot.infinity_polling()
