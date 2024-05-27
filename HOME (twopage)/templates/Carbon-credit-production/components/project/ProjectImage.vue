<template>
	<div class="flex items-center flex-wrap gap-3">
		<template v-if="editMode">
			<label for="images-upload" class="w-20 h-20 bg-gray-200 hover:bg-gray-300 border border-dashed border-gray-400 shadow-sm rounded flex items-center justify-center cursor-pointer">
				<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
					<path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
				</svg>
			</label>
			<input type="file" id="images-upload" accept="image/png,image/jpeg," multiple="multiple" class="hidden" @change="upload" />
		</template>

		<template v-if="form.project_picture.length > 0">
			<div class="relative" v-for="(img, i) in picturesItems" :key="i">
				<div v-if="editMode" @click="$emit('removeImage', i)" class="text-red-500 absolute z-20 -top-2 -right-2 bg-gray-100 rounded-full border border-red-500 hover:bg-red-500 hover:text-white cursor-pointer">
					<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4">
						<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
					</svg>
				</div>
				<div @click="showImage(i)" class="bg-white shadow-sm rounded w-20 h-20 cursor-pointer">
					<!-- {{ form.project_picture[i] }} -->
					<div v-if="form.project_picture.length > imageAmount && i == imageAmount - 1 && !editMode" class="w-full h-full bg-white opacity-60 absolute z-10 flex items-center justify-center text-black font-bold cursor-pointer">+{{ form.project_picture.length - imageAmount }} รูป</div>
					<img :src="imageUrl(img.src)" class="w-20 h-20 object-cover object-center shadow-lg rounded" />
				</div>
			</div>
		</template>

		<!-- <div @click="showImage(6)" v-if="form.project_picture.length > 6" class="bg-white shadow-sm rounded w-20 h-20 relative">
			<div class="w-full h-full bg-white opacity-60 absolute z-10 flex items-center justify-center">+{{ form.project_picture.length - 6 }} รูป</div>
			<img :src="imageUrl(form.project_picture[6].src)" class="w-full object-cover object-center" />
		</div> -->
		<client-only placeholder="loading...">
			<EasyLightBox :imgs="previewImg" :visible="visible" :index="index" @hide="visible = false"> </EasyLightBox>
		</client-only>
	</div>
</template>

<script>
import EasyLightBox from "vue-easy-lightbox";
import uploadImage from "../../static/mixins/upload-image";
export default {
	props: ["form", "editMode"],
	mixins: [uploadImage],
	components: {
		EasyLightBox,
	},
	computed: {
		picturesItems() {
			let arr = [];
			if (!this.editMode) {
				if (this.form.project_picture.length > this.imageAmount - 1) {
					for (let i = 0; i < this.imageAmount; i++) {
						arr.push(this.form.project_picture[i]);
					}
				} else {
					for (let i = 0; i < this.form.project_picture.length; i++) {
						arr.push(this.form.project_picture[i]);
					}
				}
				return arr;
			}
			return this.form.project_picture;
		},
		previewImg() {
			let arr = [];
			arr = this._.map(this.form.project_picture, (item) => {
				const newUrl = process.env.baseUrl + item.src;
				return {
					src: newUrl,
					name: item.name,
				};
			});
			return arr;
		},
	},
	data() {
		return {
			image: "",
			imageAmount: 7,

			visible: false,
			index: 0,
			loading: true,
		};
	},
	mounted() {
		if (!this.editMode) {
			this.imageAmount = 8;
		}
	},
	methods: {
		showImage(index) {
			this.index = index;
			this.visible = true;
		},

		imageUrl(url) {
			// console.log(process.env.imgUrl);
			return process.env.baseUrl + url;
		},

		async upload(input) {
			const app = this;
			const fileLength = input.target.files.length;
			for (let i = 0; i < fileLength; i++) {
				const formData = new FormData();
				const fileItem = input.target.files[i];
				// console.log(fileItem);
				formData.append("file", fileItem);
				const resp = await app.uploadImages(formData);
				// console.log(resp);
				this.$emit("saveImage", resp);
				const reader = new FileReader();
				reader.onload = function (e) {
					// app.fileArr.push(e.target.result);
				};

				reader.readAsDataURL(fileItem);
			}
		},
	},
};
</script>

<style>
</style>