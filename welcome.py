import bredis
from mwt import MWT

def set_welc_self(bot, update, args):
    uid = update.message.from_user.id
    welc_msg = args
    set_welc(bot, update, uid, welc_msg)
    resp = "Your welcome message was set to:\n{}" 
    update.message.reply_text(resp.format(bredis.getwelc(uid)), quote=False, parse_mode='Markdown')

def set_welc_other(bot, update, args):
    adminid = update.message.from_user.id 
    isAdmin = bredis.superadmin.check(adminid)
    if isAdmin is True:
        uid = args[0]
        del args[0]
        welc_msg = args
        set_welc(bot, update, uid, welc_msg)
        msg = "`{0}`'s welcome message set to:\n{1}" 
        update.message.reply_text(msg.format(uid, bredis.getwelc(uid)), quote=False, parse_mode='Markdown')
    else:
        update.message.reply_text('who are you? my lordy told me never to talk to strangers... *runs away*', quote=False)

def set_welc(bot, update, uid, message):
    user = update.message.from_user
    welc_msg = ' '.join(message)
    bredis.setwelc(welc_msg, uid)
    if user.id == uid:
        log_msg = "{fname} {lname} (`{uid}`) (@{username}) has set their welcome message to:\n {welc}"
    else: 
        log_msg = "{fname} {lname} (`{setter_id}`) (@{username}) has set `{uid}`'s welcome message to:\n {welc}"
    bot.sendMessage("@benthelog", log_msg.format(fname=user.first_name, lname=user.last_name, setter_id=user.id, uid=uid, username=user.username, welc=welc_msg), parse_mode='Markdown')

def rem(bot, update, args):
    adminid = update.message.from_user.id 
    isAdmin = bredis.superadmin.check(adminid)
    if isAdmin is True:
        uid = args[0]
        bredis.remwelc(uid)
        msg = "`{0}`'s welcome message deleted" 
        update.message.reply_text(msg.format(uid), quote=False, parse_mode='Markdown')
    else:
        update.message.reply_text('who are you? my lordy told me never to talk to strangers... *runs away*', quote=False)

def get(bot, update, args):
    isAdmin = bredis.superadmin.check(update.message.from_user.id)
    if isAdmin is True:
        if update.message.reply_to_message is not None:
            uid = update.message.reply_to_message.from_user.id
        else:
            uid = int(args[0])
        welc = bredis.getwelc(uid)
        msg = "This is `{0}`'s welcome message:\n{1}".format(uid, welc)
        update.message.reply_text(msg, quote=False, parse_mode='Markdown')
    else:
        update.message.reply_text('who are you? my lordy told me never to talk to strangers... *runs away*', quote=False)

def groupset(bot, update, args):
    user = update.message.from_user
    gid = update.message.chat.id
    if update.message.from_user.id in get_admin_ids(bot, update.message.chat_id):
        bredis.setwelc(' '.join(args), gid)
        msg = "Group welcome message set to:\n{0}" 
        update.message.reply_text(msg.format(bredis.getwelc(gid)), quote=False, parse_mode='HTML')
    else:
        update.message.reply_text('uhh...{0} i dont think youre an admin...'.format(update.message.from_user.first_name), quote=False, parse_mode='HTML')
        return None
        
@MWT(timeout=60*60)
def get_admin_ids(bot, chat_id):
        """Returns a list of admin IDs for a given chat. Results are cached for 1 hour."""
        return [admin.user.id for admin in bot.getChatAdministrators(chat_id)]

def msg(bot, update):
    user = update.message.new_chat_member
    rawwelc = bredis.getwelc(user.id)
    uid = user.id
    welc = "{0} `({1})`".format(rawwelc, uid)
    exists = bredis.exists(user.id)
    if rawwelc != None and exists == 1: 
        welc = "{0} `({1})`".format(rawwelc, uid)
        update.message.reply_text(welc, quote=False, parse_mode='Markdown')
    else: 
        groupwelc = bredis.getwelc(update.message.chat.id).format(fname=user.first_name, lname=user.last_name, uid=user.id, username=user.username)
        if groupwelc != None:
            try:
                update.message.reply_text(groupwelc, quote=False, parse_mode='Markdown')
            except:
                update.message.reply_text(groupwelc, quote=False)#, parse_mode='HTML')
        else:
            return None 

