<template>
	<div class="grid grid-cols-1 gap-2 my-2">
		<div class="col-span-1">
			<label for="retire-choice-one" class="cursor-pointer flex justify-between">
				<div class="w-full flex items-center gap-2 border p-4">
					<svg v-if="form.retirementPurposeOption != 1" width="20" height="20" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
						<circle cx="8" cy="8" r="7.5" stroke="#00B2D9" />
					</svg>
					<svg v-else width="20" height="20" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
						<circle cx="8" cy="8" r="7.5" stroke="#00B2D9" />
						<circle cx="8" cy="8" r="5" fill="#00B2D9" />
					</svg>
					<p class="text-sm font-medium">{{ $t("credit.modal.offset_emissions") }}</p>
				</div>
			</label>
			<input hidden type="radio" id="retire-choice-one" name="retire-option" :value="1" v-model="form.retirementPurposeOption" class="w-5 h-5" />
			<div v-if="form.retirementPurposeOption === 1" class="w-full bg-white border p-4">
				<UILabel :text="$t('credit.modal.on_behalf_of')" :required="false" />
				<!-- <UIDropdown v-model="form.retirementOnBehalfOf" /> -->
				<UITextInput v-model="form.retirementOnBehalfOf" />
			</div>
		</div>
		<div class="col-span-1">
			<label for="retire-choice-two" class="cursor-pointer flex justify-between">
				<div class="w-full flex items-center gap-2 border p-4">
					<svg v-if="form.retirementPurposeOption != 2" width="20" height="20" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
						<circle cx="8" cy="8" r="7.5" stroke="#00B2D9" />
					</svg>
					<svg v-else width="20" height="20" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
						<circle cx="8" cy="8" r="7.5" stroke="#00B2D9" />
						<circle cx="8" cy="8" r="5" fill="#00B2D9" />
					</svg>
					<p class="text-sm font-medium">{{ $t("credit.modal.result_base_payment") }}</p>
				</div>
			</label>
			<input hidden type="radio" id="retire-choice-two" name="retire-option" :value="2" v-model="form.retirementPurposeOption" class="w-5 h-5" />
			<div v-if="form.retirementPurposeOption === 2" class="w-full bg-white border p-4">
				<UILabel :text="$t('credit.modal.on_behalf_of')" :required="true" />
				<!-- <UIDropdown v-model="form.retirementOnBehalfOf" /> -->
				<UITextInput v-model="form.retirementOnBehalfOf" />
				<slot name="onbehalfof"></slot>
			</div>
		</div>
		<div class="col-span-1">
			<label for="retire-choice-third" class="cursor-pointer flex justify-between">
				<div class="w-full flex items-center gap-2 border p-4">
					<svg v-if="form.retirementPurposeOption != 3" width="20" height="20" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
						<circle cx="8" cy="8" r="7.5" stroke="#00B2D9" />
					</svg>
					<svg v-else width="20" height="20" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
						<circle cx="8" cy="8" r="7.5" stroke="#00B2D9" />
						<circle cx="8" cy="8" r="5" fill="#00B2D9" />
					</svg>
					<p class="text-sm font-medium">{{ $t("credit.modal.other_purpose") }}</p>
				</div>
			</label>
			<input hidden type="radio" id="retire-choice-third" name="retire-option" :value="3" v-model="form.retirementPurposeOption" class="w-5 h-5" />
			<div v-if="form.retirementPurposeOption === 3" class="w-full bg-white border p-4 space-y-4">
				<div>
					<UILabel :text="$t('credit.modal.specify_further')" :required="true" />
					<UITextInput v-model="form.retirementOtherPurpose" />
					<slot name="otherpurpose"></slot>
				</div>
				<div>
					<UILabel :text="$t('credit.modal.on_behalf_of')" :required="false" />
					<!-- <UIDropdown v-model="form.retirementOnBehalfOf" /> -->
					<UITextInput v-model="form.retirementOnBehalfOf" />
				</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	props: ["form"],
};
</script>

<style>
</style>