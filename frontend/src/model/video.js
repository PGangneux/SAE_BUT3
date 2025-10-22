export default class video {
    uuid
    url
    param_visible
    pos_x_iframe
    pos_y_iframe
    lecteur

    constructor() {
        this.param_visible = false
        this.pos_x_iframe = 0
        this.pos_y_iframe = 0
        this.lecteur = 'Viméo'
        this.url = "https://player.vimeo.com/video/1128762950?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479"
    }
}