import instaloader
import datetime
from configs.config import Config

class PostContent():
    def __init__(self, type, url, video_url=None):
        self.type = type
        self.url = url
        self.video_url = video_url
        
class PostItem():
    def __init__(self, caption:str, hashtags: list, code: str, post_items: list, date_local: datetime, date_utc: datetime):
        self.caption = caption
        self.hashtags = hashtags
        self.code = code   
        self.post_items = post_items   
        self.date_local = date_local   
        self.date_utc = date_utc   

class InstagramItem():
    def __init__(self, username):
        config = Config.get_config() 

        ig_loader = instaloader.Instaloader()
        #ig_loader.login('XXX', 'XXX')
        self.profile = instaloader.Profile.from_username(ig_loader.context, username)
    
    def get_user_profile(self):
        return {
            'username': self.profile.username,
            'fullname': self.profile.full_name,
            'biography': self.profile.biography,
            'thumbnail': self.profile.profile_pic_url
        }
    
    def get_latest_post(self, ignore_pinned=True):
        posts_iterator = self.profile.get_posts()
          
        #最後latest_posts_count個貼文
        latest_posts = []
        latest_posts_count = 4 if ignore_pinned else 1
        for _ in range(latest_posts_count):
            post = next(posts_iterator)
            latest_posts.append(post)
        dates = [post.date for post in latest_posts]
        latest_date = max(dates)
    
        # 最後一個貼文
        latest_post = latest_posts[dates.index(latest_date)] 
        #latest_post = latest_posts[2] 

        # 製作PostItem      
        post_contents = []
        if latest_post.typename == 'GraphSidecar':
            for node in latest_post.get_sidecar_nodes():
                if node.is_video:
                    post_contents.append(
                        PostContent('video', node.display_url, node.video_url))
                else:
                    post_contents.append(
                        PostContent('image', node.display_url))
        else:
            # 單張圖片或單部影片
            if latest_post.is_video:
                post_contents.append(
                    PostContent('video', latest_post.url, latest_post.video_url))
            else:
                post_contents.append(
                    PostContent('image', latest_post.url))
        return PostItem(
            latest_post.caption, 
            latest_post.caption_hashtags, 
            latest_post.shortcode,
            post_contents,
            latest_post.date_local,
            latest_post.date_utc)