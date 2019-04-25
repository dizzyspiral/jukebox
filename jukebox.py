import tornado.ioloop
import tornado.web
import queues
import player
import downloader

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        playlist = "Playlist:\n\n"

        for i in range(len(queues.play_queue)):
            playlist += str(i) + ". " + str(queues.play_queue[i]) + "\n"

        print(playlist)

        self.write(playlist)

class QueueHandler(tornado.web.RequestHandler):
    def get(self, video_uri):
        queues.download_lock.acquire()

        try:
            url = "https://www.youtube.com/watch?v=" + str(video_uri)
            queues.download_queue.append(str(url))
            self.write("Added URL '" + str(url) + "' to the download queue.\n")
        except:
            print("Unable to queue download url '" + str(url) + "'\n")
            self.write("Unable to add URL '" + str(url) + "' to the download queue.\n")
        finally:
           queues.download_lock.release()

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/queue/(.*)", QueueHandler)
    ])

if __name__ == "__main__":
    downloadthread = downloader.DownloadThread()
    playthread = player.PlayThread()

    downloadthread.start()
    playthread.start()

    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
