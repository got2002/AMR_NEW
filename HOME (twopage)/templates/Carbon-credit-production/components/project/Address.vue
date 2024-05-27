<template>
	<section>
		<div class="grid grid-cols-1 gap-2 text-sm">
			<div class="col-span-1 flex flex-col" v-for="(address, i) in form.address" :key="i">
				<div class="flex items-center">
					<!-- <label class="w-32 px-3 py-2 text-center border-2 bg-gray-200">{{ $t("project.create_page.address.subtitle") }} ({{ i + 1 }})</label> -->
					<input v-model="form.address[i]" type="text" class="w-full px-3 py-2 text-center border-2" />
					<!-- <button v-if="form.address.length > 1" @click="$emit('deleteAddress', i)" class="py-2 px-2 border-2 border-red-500 bg-red-500 text-white">X</button> -->
				</div>
				<span class="text-left text-red-500" v-if="!$v.form.address.$each[i].required && isSubmitted">{{ $t("project.create_page.form_validation.address") }}</span>
			</div>
		</div>
	</section>
</template>

<script>
import { required } from "vuelidate/lib/validators";
export default {
	props: ["form","isSubmitted"],
	
	validations() {
		return {
			form: {
				address: {
					$each: { required },
				},
			},
		};
	},
};
</script>

<style>
</style>