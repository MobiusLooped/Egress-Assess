'''

This is for functions potentially used by all modules

'''

import argparse
import os
import random
import re
import string
import sys
import time


def cli_parser():
    # Command line argument parser
    parser = argparse.ArgumentParser(
        add_help=False,
        description="The Egress-Assess is a tool used to assess egress filters\
        protecting a network")
    parser.add_argument(
        '-h', '-?', '--h', '-help', '--help', action="store_true",
        help=argparse.SUPPRESS)

    protocols = parser.add_argument_group('Client Protocol Options')
    protocols.add_argument(
        "--client", default=None, metavar="[http]",
        help="Extract data over the specified protocol.")
    protocols.add_argument(
        "--list-clients", default=False, action='store_true',
        help="List all supported client protocols.")
    protocols.add_argument("--ip", metavar="192.168.1.2", default=None,
                           help="IP to extract data to.")

    protocols = parser.add_argument_group('Actor Emulation')
    protocols.add_argument(
        "--actor", default=None, metavar="[zeus]",
        help="Emulate [actor] C2 comms to egress server.")

    servers = parser.add_argument_group('Server Protocol Options')
    servers.add_argument(
        "--server", default=None, metavar='[http]',
        help="Create a server for the specified protocol.")
    servers.add_argument("--list-servers", default=False, action='store_true',
                         help="Lists all supported server protocols.")

    ftp_options = parser.add_argument_group('FTP Options')
    ftp_options.add_argument(
        "--username", metavar="testuser", default=None,
        help="Username for FTP server authentication.")
    ftp_options.add_argument(
        "--password", metavar="pass123", default=None,
        help="Password for FTP server authentication.")

    data_content = parser.add_argument_group('Data Content Options')
    data_content.add_argument(
        "--file", default=None, metavar='/root/test.jpg',
        help="Path to file for exfiltration via Egress-Assess.")
    data_content.add_argument(
        "--datatype", default=None, metavar='[ssn]',
        help="Extract data containing fake social security numbers.")
    data_content.add_argument(
        "--data-size", default=1, type=int,
        help="Number of megs to send")
    data_content.add_argument(
        "--list-datatypes", default=False, action='store_true',
        help="List all data types that can be generated by the framework.")

    args = parser.parse_args()

    if args.h:
        parser.print_help()
        sys.exit()

    if ((args.server == "ftp" or args.server == "sftp") or (
            args.client == "ftp" or args.client == "sftp")) and (
            args.username is None or args.password is None):
        print "[*] Error: FTP or SFTP connections require \
            a username and password!".replace('    ', '')
        print "[*] Error: Please re-run and provide the required info!"
        sys.exit()

    if args.client and args.ip is None:
        print "[*] Error: You said to act like a client, but provided no ip"
        print "[*] Error: to connect to.  Please re-run with required info!"
        sys.exit()

    if (args.client is not None) and (args.datatype is None) and (
            args.file is None):
        print "[*] Error: You need to tell Egress-Assess the type \
            of data to send!".replace('    ', '')
        print "[*] Error: to connect to.  Please re-run with required info!"
        sys.exit()

    if (args.client is None and args.server is None and
            args.list_servers is None and args.list_clients is None and
            args.list_datatypes is None):
        print "[*] Error: You didn't tell Egress-Assess to act like \
            a server or client!".replace('    ', '')
        print "[*] Error: Please re-run and provide an action to perform!"
        parser.print_help()
        sys.exit()

    return args


def randomNumbers(b):
    """
    Returns a random string/key of "b" characters in length, defaults to 5
    """
    random_number = int(''.join(random.choice(string.digits) for x in range(b))
                        ) + 10000

    if random_number < 100000:
        random_number = random_number + 100000

    return str(random_number)


def randomString(length=-1):
    """
    Returns a random string of "length" characters.
    If no length is specified, resulting string is in between 6 and 15 characters.
    """
    if length == -1:
        length = random.randrange(6, 16)
    random_string = ''.join(random.choice(string.ascii_letters) for x in range(length))
    return random_string


def title_screen():
    os.system('clear')
    print "#" * 80
    print "#" + " " * 32 + "Egress-Assess" + " " * 33 + "#"
    print "#" * 80 + "\n"
    return


def ea_path():
    return os.getcwd()


def validate_ip(val_ip):
    # This came from (Mult-line link for pep8 compliance)
    # http://python-iptools.googlecode.com/svn-history/r4
    # /trunk/iptools/__init__.py
    ip_re = re.compile(r'^(\d{1,3}\.){0,3}\d{1,3}$')
    if ip_re.match(val_ip):
        quads = (int(q) for q in val_ip.split('.'))
        for q in quads:
            if q > 255:
                return False
        return True
    return False


def writeout_text_data(incoming_data):
    # Get the date info
    current_date = time.strftime("%m/%d/%Y")
    current_time = time.strftime("%H:%M:%S")
    file_name = current_date.replace("/", "") +\
        "_" + current_time.replace(":", "") + "text_data.txt"

    # Write out the file
    with open(ea_path() + "/" + file_name, 'w') as out_file:
        out_file.write(incoming_data)

    return file_name

malware_uris = [
    '/jm32/includes/site/bot.exe', '/jm32/includes/site/config.bin',
    '/jm32/includes/site/gate.php', '/mathew/config.jpg',
    '/docs/.docs/config.jpg', '/docs/.docs/do.php',
    '/zeujuus/a/gate.php', '/zeujuus/a/modules/bot.exe',
    '/zeujuus/a/modules/config.bin',
    '/zejius/2HZG41Zw/6Vtmo6w4yQ5tnsBHms64.php',
    '/zejius/2HZG41Zw/bot.exe',
    '/zejius/2HZG41Zw/fJsnC6G4sFg2wsyn4shb.bin',
    '/zejius/5GPR0iy9/6Vtmo6w4yQ5tnsBHms64.php',
    '/zejius/5GPR0iy9/bot.exe',
    '/zejius/5GPR0iy9/fJsnC6G4sFg2wsyn4shb.bin', '/past/config.jpg',
    '/past/gate.php', '/fan/base/config.jpg',
    '/wp-includes/pomo/panel/config.jpg',
    '/wp-includes/pomo/panel/gate.php', '/themes/panel/config.jpg',
    '/themes/panel/gate.php', '/home/libraries/joomla/php/gate.php',
    '/home/plugins/system/tmp/bot.scr',
    '/home/plugins/system/tmp/config.bin',
    '/home/plugins/system/tmp/gate.php', '/js/ssj/config.jpg',
    '/js/ssj/gate.php', '/site/tmp/xml/config.jpg',
    '/site/tmp/xml/gate.php', '/news/wpg.php', '/file.php',
    '/.cgi-bin./as.bin', '/wp-content/themes/bmw_lab/new.ban',
    '/wp-content/themes/bmw_lab/newnew.wav', '/vs/panel/config.jpg',
    '/vs/panel/gate.php', '/brand/server/file.php',
    '/brand/server/gate.php',
    '/wp-admin/css/colors/sunrise/admin/bot.exe',
    '/wp-admin/css/colors/sunrise/admin/config.bin',
    '/wp-admin/css/colors/sunrise/admin/secure.php',
    '/wp-content/themes/chagim/library/images/plates/bot.exe',
    '/wp-content/themes/chagim/library/images/plates/config.bin',
    '/wp-content/themes/chagim/library/images/plates/gate.php',
    '/images/burr_insurance001001.php', '/images/team/config.jpg',
    '/images/team/gate.php', '/test/config.jpg', '/test/gate.php',
    '/ray/server/file.php', '/ray/server/gate.php', '/capa.bin',
    '/capa.exe', '/secure.php', '/ral/30/config.bin',
    '/ral/30/secure.php', '/wp-admin/css/config.bin',
    '/wp-admin/css/gate.php', '/wp-admin/css/setup.exe',
    '/panel/config.jpg', '/panel/gate.php',
    '/wp-includes2/SimplePie/Net/page/config.jpg',
    '/wp-includes2/SimplePie/Net/page/gate.php',
    '/includes/.srv/srv/bot.exe',
    '/includes/.srv/srv/config.bin', '/includes/.srv/srv/gate.php',
    '/ric/30/config.bin', '/ric/30/secure.php', '/blog/crea.bin',
    '/blog/crea.exe', '/blog/secure.php', '/images2/dave.jpg',
    '/images2/gate.php', '/wp-includes/ID3/config.jpg',
    '/wp-includes/ID3/gate.php', '/emman/panel/config.jpg',
    '/emman/panel/gate.php', '/xampp/img/escu.bin',
    '/xampp/img/escu.exe', '/xampp/img/secure.php',
    '/.css/config.jpg', '/.css/gate.php', '/admin/cfg.bin',
    '/admin/gate.php', '/isai/modules/mod_upgrade/bot.exe',
    '/isai/modules/mod_upgrade/config.bin',
    '/isai/modules/mod_upgrade/gate.php', '/wp-comment/firs.jpg',
    '/wp-comment/gate.php', '/panel/file.php', '/panel/gate.php',
    '/images01/fong.bin', '/images01/fong.exe', '/images01/gate.php',
    '/img/vg.php', '/components/com_file/file.php',
    '/components/com_file/gate.php', '/images/panel/config.jpg',
    '/images/panel/gate.php', '/wordpress/gate.php',
    '/wordpress/gree.jpg', '/media/.tmp/file.php',
    '/media/.tmp/gate.php', '/gate.php', '/modules/holl.bin',
    '/modules/holl.exe', '/templates/admin/install/config.jpg',
    '/templates/admin/install/gate.php',
    '/tmp/admin/install/config.jpg', '/tmp/admin/install/gate.php',
    '/tmp/cp/config.jpg', '/tmp/cp/gate.php',
    '/tmp/install/config.jpg', '/tmp/install/gate.php',
    '/frank/panel/config.jpg', '/frank/panel/gate.php',
    '/tmp/configs/new/vg.php', '/meask/lite/file.php',
    '/meask/lite/gate.php', '/css/src/admin/config.jpg',
    '/css/src/admin/gate.php', '/js/admin/install/config.jpg',
    '/js/admin/install/gate.php',
    '/wp-content/plugins/wp-db-backup-made/work.php',
    '/update/bot.exe', '/update/cfg.bin', '/update/gate.php',
    '/chopinschumann/ital.bin', '/chopinschumann/ital.exe',
    '/chopinschumann/secure.php', '/images/ital.bin',
    '/images/ital.exe', '/images/secure.php',
    '/compose/panel/bot.exe', '/compose/panel/config.bin',
    '/compose/panel/secure.php', '/fy97/panel/config.bin',
    '/fy97/panel/secure.php', '/images/joea.bin', '/images/joea.exe',
    '/images/secure.php', '/components/com_joomla/plugin/config.jpg',
    '/components/com_joomla/plugin/gate.php',
    '/resource/css/config.bin', '/resource/css/secure.php',
    '/wp-content/upgrade/PANEL/config.jpg',
    '/wp-content/upgrade/PANEL/gate.php',
    '/wp-content/plugins/bcet56aoikqf52iu/food.php',
    '/Scripts/_notes/build/bot.exe',
    '/Scripts/_notes/build/config.bin',
    '/Scripts/_notes/build/gate.php', '/REMOVED/.pop/bot.exe',
    '/REMOVED/.pop/config.bin', '/REMOVED/.pop/gate.php',
    '/KINS/panel/bot.exe', '/KINS/panel/config.jpg',
    '/KINS/panel/gate.php', '/panel/config.jpg', '/panel/gate.php',
    '/walex/files/bot.exe', '/walex/files/config.jpg',
    '/walex/files/gate.php', '/e7/bot.exe', '/e7/cfg.bin',
    '/e7/gate.php',
    '/wp-admin/css/colors/coffee/cat/server/config.jpg',
    '/wp-admin/css/colors/coffee/cat/server/gate.php',
    '/site/S/13897652/5112/file.php',
    '/site/S/13897652/5112/gate.php',
    '/images/js/osomo/panel/config.jpg',
    '/images/js/osomo/panel/gate.php',
    '/themes/panel/config.jp', '/themes/panel/gate.php',
    '/system/eusat/telesa/config.jpg', '/sadcxvbv/vdfbffddf.php',
    '/wqwcqqw/sasasacw.php', '/images/server/file.php',
    '/images/server/gate.php', '/cache/lcitorg/config.bin',
    '/cache/lcitorg/gate.php', '/form/panel/config.jpg',
    '/form/panel/gate.php', '/backup/gate.php',
    '/backup/jera.jpg', '/images/file.php',
    '/images/js/panel/config.jpg', '/images/js/panel/gate.php',
    '/images/config.jpg', '/images/gate.php',
    '/slim-cita/helps/file.php', '/slim-cita/helps/gate.php',
    '/kin/panelz/config.jpg', '/kin/panelz/gate.php',
    '/image/Panel/config.jpg', '/folder/config.bin',
    '/folder/secure.php', '/plugins/panel/config.jpg',
    '/plugins/panel/gate.php',
    '/wp-content/plugins/slxcdfrdmn9r0x/j7.php', '/q/gate.php',
    '/q/outl.jpg', '/media/k2/file.php', '/media/k2/gate.php',
    '/js/MOM/config.jpg', '/js/MOM/gate.php',
    '/lung/panel/config.jpg', '/wp/config.jpg',
    '/wp/gate.php', '/data/config.jpg', '/data/gate.php',
    '/templates/beez/bot.exe', '/templates/beez/config.bin',
    '/templates/beez/gate.php', '/wp-includes/css/new/config.jpg',
    '/wp-includes/css/new/gate.php',
    '/language/pdf_fonts/server/bot.exe',
    '/language/pdf_fonts/server/config.bin',
    '/language/pdf_fonts/server/gate.php', '/js/liscence.php',
    '/js/userslogin.php', '/ijo/config.jpg', '/ijo/gate.php',
    '/Mix/valeg/bot.exe', '/Mix/valeg/config.bin',
    '/Mix/valeg/gate.php', '/media/media/js/.js/ajax.php',
    '/media/media/js/.js/color.jpg', '/wpc/Panel/config.jpg',
    '/wpc/Panel/gate.php', '/images/gate.php', '/images/stab.jpg',
    '/wpadm/Panel/config.jpg', '/wpadm/Panel/gate.php',
    '/admin/b7.php', '/admin/file.php', '/amed/config.jpg',
    '/amed/gate.php', '/sadcxvbv/vdfbffddf.php',
    '/wpimages/image.php', '/ger/config.jpg', '/ger/gate.php',
    '/percy/panel/config.jpg', '/percy/panel/gate.php',
    '/map/Icons/outglav.exe', '/map/Icons/Religion/brah.png',
    '/map/Icons/Religion/exejfjfjexe.exe', '/images/config.jpg',
    '/images/gate.php', '/file.php', '/gate.php', '/.css/config.jpg',
    '/.css/gate.php', '/colobus/gate.php', '/colobus/vsam.jpg',
    '/news/secure.php', '/news/vuan.bin', '/.id/file.php',
    '/.id/gate.php',
    '/fast-move/cidphp/file.php', '/fast-move/cidphp/gate.php',
    '/overopen/panel/config.bin', '/overopen/panel/secure.php',
    '/chromez/config.jpg', '/chromez/gate.php', '/libraries/db.php',
    '/sadcxvbv/vdfbffddf.php', '/wqwcqqw/sasasacw.php',
    '/wp-comment/baba.jpg', '/wp-comment/gate.php',
    '/alumno309/images/base.bin', '/alumno309/images/base.exe',
    '/alumno309/images/secure.php',
    '/wp-content/plugins/wp-db-backup-made/das.db',
    '/ta_images/tools.php', '/plank/panel/config.jpg',
    '/includes/database/http/config.jpg',
    '/includes/database/http/zin.php', '/wqwcqqw/sasasacw.php',
    '/administrator/modules/mod_menu/help/config.jpg',
    '/administrator/modules/mod_menu/help/gate.php', '/old/jx36.bin',
    '/old/jx36.exe', '/old/secure.php', '/images/icons/bt.exe',
    '/images/icons/cfg.bin', '/images/icons/gate.php', '/t/wpg.php',
    '/forum.php', '/config.php', '/wp-blog/gate.php',
    '/wp-blog/mell.jpg', '/descargas/adm/gate.php',
    '/descargas/config/orqu.bin', '/wp-rss.php', '/images/gate.php',
    '/images/outl.jpg', '/images/smilies/raye.jpg',
    '/images/kin/config.jpg', '/jaextmanager_data/rimm.bin',
    '/jaextmanager_data/secure.php', '/js/cssme/file.php',
    '/js/cssme/thread.php', '/mss/plugins/system/config.bin',
    '/mss/plugins/system/gate.php', '/wp-admin/maint/config.bin',
    '/wp-admin/maint/gate.php', '/blog/wp-content/uploads/kim.dot',
    '/images/secure.php', '/images/todo.bin', '/images/todo.exe',
    '/plugins/system/bot.exe', '/plugins/system/config.bin',
    '/plugins/system/gate.php', '/modules/mod_footer/tmpl/file.php',
    '/modules/mod_footer/tmpl/gate.php', '/modules/secure.php',
    '/modules/warp.bin', '/modules/warp.exe', '/file.php',
    '/gate.php', '/db1/config.jpg', '/db1/gate.php',
    '/katolog/thumbs/panel/config.jpg',
    '/katolog/thumbs/panel/gate.php']