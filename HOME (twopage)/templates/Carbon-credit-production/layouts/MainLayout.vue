<template>
	<div class="flex">
		<div v-if="isShowNotice" class="fixed top-0 left-0 w-full h-full bg-black bg-opacity-50 backdrop-filter backdrop-blur-sm" style="z-index: 5000">
			<div class="flex items-center justify-center h-full">
				<div class="xl:w-6/12 lg:w-7/12 w-8/12">
					<div class="bg-white shadow-md rounded">
						<img src="/images/carbonmarket-01.jpg" class="w-full scale-90 object-cover object-center" />
						<div class="p-2">
							<label for="show-notice" class="inline-flex items-center gap-2 text-sm">
								<input v-model="isShowAgain" @change="showNoticeEvent" type="checkbox" id="show-notice" :value="true" />
								<span>{{$t('not_show_again')}}</span>
							</label>
						</div>
					</div>

					<div class="text-center mt-4">
						<button @click="isShowNotice = false" class="px-4 py-2 bg-carbon-blue-logo rounded shadow-md text-white">{{ $t("button.close") }}</button>
					</div>
				</div>
			</div>
		</div>
		<div class="bg-theme-black-50 w-full">
			<TopNav />

			<div class="2xl:px-60 p-2 md:p-10 w-full bg-theme-black-50">
				<Nuxt />
			</div>
		</div>
	</div>
</template>
<script>
export default {
	data: () => ({
		isShowAgain: false,
		isShowNotice: false,
	}),
	computed:{
		dataFromStorage(){
			return this.$auth.$storage.getLocalStorage("isShowAgain")
		}
	},
	mounted() {
		
		if(this.dataFromStorage === null || !this.dataFromStorage){
			this.isShowNotice = true
			this.showNoticeEvent()
		}
		else this.isShowNotice = false
		
	},
	methods: {
		showNoticeEvent() {
			this.$auth.$storage.setLocalStorage("isShowAgain", this.isShowAgain);
		},
	},
};
</script>
