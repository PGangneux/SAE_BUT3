<script>
import { markRaw } from 'vue';
import Tag from '../../model/tag';

export default {
    name: "tags",
    props: {
        video: {
            type: Object,
            required: true
        }
    },
    computed: {
        tagExistsInDatabase() {
            return markRaw(this.liste_tags_bd.some(tag => 
                tag.name.toLowerCase() === this.newTagName.trim().toLowerCase()
            ));
        },
        tagAlreadyInVideo() {
            return markRaw(this.liste_tags_video.some(tag => 
                tag.name.toLowerCase() === this.newTagName.trim().toLowerCase()
            ));
        },
        isValidTagName() {
            return this.newTagName.trim().length > 0;
        }
    },
    data() {
        return {
            liste_tags_video: [],
            liste_tags_bd: [],
            allTags: [],
            newTagName: '', // For the input field
        }
    },
    async mounted() {
        await this.loadTags();
    },
    methods: {
        async loadTags() {

            this.liste_tags_video = markRaw(await this.video.tags());
            this.allTags = markRaw(await Tag.list());


            // Filter out tags that are already associated with the video
            this.liste_tags_bd = markRaw(this.allTags.filter(tag => 
                !this.liste_tags_video.some(videoTag => videoTag.uuid === tag.uuid)
            ));

        },
        
        async addTag() {
            // Find the tag in the available list
            const tag = this.liste_tags_bd.find(t => t.name === this.newTagName);
            if (tag) {
                await this.video.connect_tag(tag);
                await this.loadTags(); // Reload tags
                this.newTagName = '';
            }
        },
        
        async createTag() {
            if (this.newTagName.trim()) {
                // Create new tag (adjust based on your Tag model's create method)
                const newTag = await markRaw(new Tag({name:this.newTagName})).create();
                // Add it to the video
                await this.video.connect_tag(newTag);
                await this.loadTags(); // Reload tags
                this.newTagName = '';
            }
        },
        
        async removeTag(tag) {
            // Remove tag from video (you'll need to implement this method)
            await this.video.disconnect_tag(tag);
            await this.loadTags(); // Reload tags
        }
    }
};
</script>

<template>
    <div>
        <h1>Tags</h1>

        <div>
            <input 
                type="text" 
                v-model="newTagName"
                list="tagData"
                placeholder="Tags..." 
            />
            <datalist id="tagData">
                <option 
                    v-for="tag in liste_tags_bd" 
                    :key="tag.uuid" 
                    :value="tag.name"
                />
            </datalist>
            <button 
                :disabled="tagExistsInDatabase || !isValidTagName || tagAlreadyInVideo" 
                @click="createTag"
            >
                Créer
            </button>
            <button 
                :disabled="!tagExistsInDatabase || !isValidTagName || tagAlreadyInVideo" 
                @click="addTag"
            >
                Ajouter
            </button>
            
        </div>
        <div class="champ_tags">
            <ul>
                <li v-for="tag in liste_tags_video" :key="tag.uuid">
                    {{ tag.name }}
                    <button @click="removeTag(tag)" class="btn-remove">✕</button>
                </li>
            </ul>
        </div>
    </div>
</template>

<style scoped>
h1 {
    text-align: center;
}

button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.champ_tags {
    min-height: 30vh;
    background-color: var(--gris-moyen);
    padding: 10px;
}

.champ_tags ul {
    list-style: none;
    padding: 0;
}

.champ_tags li {
    display: inline-block;
    padding: 5px 10px;
    margin: 5px;
    background-color: var(--vert-pale);
    border-radius: 5px;
}

.btn-remove {
    margin-left: 8px;
    background: none;
    border: none;
    cursor: pointer;
    color: #d4c6c6;
}

.btn-remove:hover {
    color: #ff0000;
}
</style>