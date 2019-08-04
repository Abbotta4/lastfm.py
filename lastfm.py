import znc, requests
import xml.etree.ElementTree as et

class lastfm(znc.Module):
    description = "Last.fm now playing command for ZNC"
    has_args = True
    args_help_text = "username,api_key"
    module_types = [znc.CModInfo.UserModule]
    username = ""
    api_key = ""

    def OnLoad(self, args, message):
        try:
            self.username = args.split(',')[0]
            self.api_key = args.split(',')[1]
            return True
        except:
            message.s = "Invalid arguments"
            return False

    def OnUserMsg(self, channel, message):
        if message.s == '.np':
            try:
                nowplaying = now_playing(self.username, self.api_key)
            except (Exception) as e:
                self.PutModNotice("Could not fetch now playing: {0}".format(str(e)))
                return znc.HALTCORE
            else:
                message.s = "Now Playing: {0}".format(nowplaying)
                self.PutModNotice(message.s)
        return znc.CONTINUE

def now_playing(username, api_key):
    try:
        feed_url = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=' + username + '&api_key=' + api_key + '&limit=1'
        r = requests.get(feed_url)
        e = et.fromstring(r.text)
        track = e.findall("./recenttracks/track/*")
        if track[4].text is not None:
            album = " [" + track[4].text + "]"
        else:
            album = ""
        return track[0].text + ' - ' + track[1].text + album
    except (TypeError, IndexError):
        raise Exception('No recent tracks found for %s' % username)
    except IOError:
        raise Exception('Couldn\'t reach last.fm')
