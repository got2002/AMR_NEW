<template>
	<div class="fixed z-50 top-0 left-0 w-full h-full bg-black bg-opacity-60 flex items-center justify-center">
		<div data-aos="fade-down" data-aos-anchor-placement="top-center" class="mx-auto container bg-white rounded shadow-sm p-4 xl:w-6/12 lg:w-8/12 md:w-10/12 w-11/12 space-y-4">
			<div class="flex justify-between items-center">
				<p class="text-xl font-bold">Serial Number</p>
				<button @click="$emit('close')" class="bg-white px-3 py-1 border border-gray-300 hover:bg-gray-50 rounded">{{ $t("button.close") }}</button>
			</div>
			<!-- <div>
				<p class="text-sm font-thin">{{ $t("home.modal.subtitle") }}</p>
			</div> -->
			<div>
				<!-- <label>Serial Number</label> -->
				<div class=" bg-gray-50 border border-gray-200">
					

					<input readonly @focus="$event.target.select()" ref="clone" :title="$t('click_copy')" @click="copyToClipboard" class="text-xl w-full h-14 bg-gray-200 text-center cursor-pointer" id="myToken" v-model="token">
				</div>
			</div>
			<!-- <div class="flex justify-end">
				<button @click="getToken()" class="px-4 py-2 rounded shadow-sm text-white bg-tgo-teal-500 hover:bg-tgo-teal-600 border border-gray-400">{{ $t("button.create_token") }}</button>
			</div> -->
		</div>
	</div>
</template>

<script>
import AOS from "aos";
import "aos/dist/aos.css";
	export default {
		props:['info'],
		data() {
			return {
				token: "",
				loading: false,
			};
		},
		mounted() {
			AOS.init();
			this.getSerial()
		},
		methods: {
			copyToClipboard() {
				const copyText = document.getElementById("myToken");
				this.$refs.clone.focus();
				try {
					document.execCommand("copy");
					this.$toast.success(this.$t("toast.copy.success"));
				} catch (error) {
					this.$toast.error(this.$t("toast.copy.fail"));
				}

				setTimeout(this.$toast.clear, 3000);
			},
			getSerial(){
				const serial = `TH1-${this.info.programID}-${this.info.project_code_id}-${this.info.day_batch_number}-${this.info.vintage_year}-${this.info.block_start}-${this.info.block_end}-${this.info.authorizedUse}-${this.info.label}`
				this.token = serial
			}
			
		},
	};
</script>

<style></style>
