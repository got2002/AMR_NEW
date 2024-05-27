<template>
	<div class="w-full">
		<div class="flex items-center bg-gray-200 rounded">
			<button @click="tab = 1" class="w-1/3 flex items-center gap-2 justify-center py-3 rounded" :class="{ 'bg-tgo-teal-500 text-white': tab == 1 }">
				<showroomLeafIcon width="24" height="24" :color="tab == 1 ? 'white' : 'black'" />
				{{ $t("project.view_page.environmental") }}
			</button>
			<button @click="tab = 2" class="w-1/3 flex items-center gap-2 justify-center py-3 rounded" :class="{ 'bg-tgo-teal-500 text-white': tab == 2 }">
				<showroomUserIcon width="24" height="24" :color="tab == 2 ? 'white' : 'black'" />
				{{ $t("project.view_page.societal") }}
			</button>
			<button @click="tab = 3" class="w-1/3 flex items-center gap-2 justify-center py-3 rounded" :class="{ 'bg-tgo-teal-500 text-white': tab == 3 }">
				<showroomCloudMoneyIcon width="24" height="24" :color="tab == 3 ? 'white' : 'black'" />
				{{ $t("project.view_page.economical") }}
			</button>
		</div>
		<div class="bg-white p-4 rounded-b">
			<div class="flex justify-start items-center w-full text-sm">
				<p  v-show="tab == 1" class="break-words list-disc list-inside whitespace-pre-line leading-snug">
					{{ environmentLang() }}
					<!-- <label class="flex items-center justify-center px-2 py-1 text-sm">{{ form.co_benefit.environment }}</label> -->
				</p>
			</div>
			<div class="flex justify-start items-center w-full text-sm">
				<p  v-show="tab == 2" class="break-words list-disc list-inside whitespace-pre-line leading-snug">
					{{ societyLang() }}
					<!-- <label class="flex items-center justify-center px-2 py-1 text-sm">{{ form.co_benefit.environment }}</label> -->
				</p>
			</div>
            <div class="flex justify-start items-center w-full text-sm">
				<p  v-show="tab == 3" class="break-words list-disc list-inside whitespace-pre-line leading-snug">
					{{ economyLang() }}
					<!-- <label class="flex items-center justify-center px-2 py-1 text-sm">{{ form.co_benefit.environment }}</label> -->
				</p>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	props:['form'],
	data() {
		return {
			tab: 1,
		};
	},
	methods:{
		economyLang(){
			if (this.$i18n.locale === "th") {
				return this.form?.co_benefit?.economy
			}
			return this.form?.co_benefit_en?.economy
		},
		societyLang(){
			if (this.$i18n.locale === "th") {
				return this.form?.co_benefit?.society
			}
			return this.form?.co_benefit_en?.society
		},
		environmentLang(){
			if (this.$i18n.locale === "th") {
				return this.form?.co_benefit?.environment
			}
			return this.form?.co_benefit_en?.environment
		},
	}
};
</script>

<style>
</style>