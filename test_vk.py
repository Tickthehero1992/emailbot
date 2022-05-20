import vk_api
from text_generator import TextGenerator
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.enums import VkUserPermissions
token = "d6ee95434a07065bdf31a2188ea373c77637ecab7c0ae161cc04aae4485599377b4d15a251b7ca0094f57"

vk_session = vk_api.VkApi(token=token) # токен получается тут https://vk.com/editapp?act=create  https://oauth.vk.com/authorize?client_id=6178269&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,messages,notify,photos,wall,email,mail,groups,stats,offline&response_type=token&v=5.74
#vk_session.auth()

vk = vk_session.get_api()

# upload = VkUpload(vk_session)  # Для загрузки изображений
# longpoll = VkLongPoll(vk_session)


# vk.messages.send(
#                     user_id=14341998,
#                     random_id=get_random_id(),
#                     message='Gey'
#                 )




#print(chat_id)
group_id = 22348657
users = vk.groups.getMembers(group_id=group_id)





