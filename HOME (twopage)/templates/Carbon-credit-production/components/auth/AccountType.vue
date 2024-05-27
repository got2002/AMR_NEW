<template>
	<div class="flex flex-col">
		<div class="w-full flex flex-col md:flex-row pt-4">
			<div class="w-full md:w-1/2 divide-y">
				<div class="pb-4">
					<p class="text-green-600">{{ $t("openAccount.account_type.title") }}</p>
					<p class="text-sm text-gray-600">{{ $t("openAccount.account_type.subtitle") }}</p>
				</div>
	
				<div class="grid grid-cols-2 gap-4 pr-0 md:pr-4 py-4 text-sm">
					<div class="col-span-1">
						<label for="guest">
							<div :class="{ 'bg-green-50 border-green-500': form.account_type == 0 }" class="w-full py-10 flex flex-col items-center justify-center bg-gray-50 border border-gray-300 rounded cursor-pointer">
								<svg width="48" height="49" viewBox="0 0 48 49" fill="none" xmlns="http://www.w3.org/2000/svg">
									<path d="M31.5 12.5C31.5 14.4891 30.7098 16.3968 29.3033 17.8033C27.8967 19.2098 25.9891 20 24 20C22.0108 20 20.1032 19.2098 18.6967 17.8033C17.2901 16.3968 16.5 14.4891 16.5 12.5C16.5 10.5109 17.2901 8.60322 18.6967 7.1967C20.1032 5.79018 22.0108 5 24 5C25.9891 5 27.8967 5.79018 29.3033 7.1967C30.7098 8.60322 31.5 10.5109 31.5 12.5ZM9.00195 40.736C9.06622 36.8007 10.6746 33.0483 13.4803 30.2881C16.286 27.5279 20.0641 25.9809 24 25.9809C27.9358 25.9809 31.7139 27.5279 34.5196 30.2881C37.3253 33.0483 38.9337 36.8007 38.998 40.736C34.2927 42.8935 29.1762 44.007 24 44C18.648 44 13.568 42.832 9.00195 40.736Z" stroke="black" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
								</svg>
								<p class="mt-4">{{ $t("openAccount.account_type.option.guest") }}</p>
							</div>
						</label>
						<input v-model="form.account_type" type="radio" id="guest" :value="0" hidden />
					</div>
					<div class="col-span-1">
						<label for="juristic">
							<div :class="{ 'bg-green-50 border-green-500': form.account_type == 1 }" class="w-full py-10 flex flex-col items-center justify-center bg-gray-50 border border-gray-300 rounded cursor-pointer">
								<svg width="48" height="49" viewBox="0 0 48 49" fill="none" xmlns="http://www.w3.org/2000/svg">
									<path d="M7.5 42.5H40.5M9 6.5H39M10.5 6.5V42.5M37.5 6.5V42.5M18 14H21M18 20H21M18 26H21M27 14H30M27 20H30M27 26H30M18 42.5V35.75C18 34.508 19.008 33.5 20.25 33.5H27.75C28.992 33.5 30 34.508 30 35.75V42.5" stroke="black" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
								</svg>
	
								<p class="mt-4">{{ $t("openAccount.account_type.option.juristic") }}</p>
							</div>
						</label>
						<input v-model="form.account_type" type="radio" id="juristic" :value="1" hidden />
					</div>
					<div class="col-span-2">
						<label for="government">
							<div :class="{ 'bg-green-50 border-green-500': form.account_type == 2 }" class="w-full py-10 flex flex-col items-center justify-center bg-gray-50 border border-gray-300 rounded cursor-pointer">
								<svg width="48" height="49" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
									<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21M3 3h12m-.75 4.5H21m-3.75 3.75h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008zm0 3h.008v.008h-.008v-.008z" />
								</svg>
	
								<p class="mt-4 text-center">{{ $t("openAccount.account_type.option.government") }}</p>
							</div>
						</label>
						<input v-model="form.account_type" type="radio" id="government" :value="2" hidden />
					</div>
					<!-- <div class="col-span-2 h-5"></div> -->
					<!-- <div class="col-span-2 hidden md:flex">
						<button @click="$emit('click')" class="w-full bg-tgo-teal-500 border shadow-md rounded text-center py-2 text-white">{{ $t("button.confirm") }}</button>
					</div> -->
				</div>
			</div>
			<div class="w-full md:w-1/2 space-y-4">
				<div>
					<p>{{ $t("openAccount.account_type.document_discription.title") }}</p>
				</div>
				<div class="w-full bg-gray-100 p-4 h-96 overflow-y-auto text-sm">
					<p class="underline">{{ $t("openAccount.account_type.document_discription.guest.title") }}</p>
					<p>1) {{ $t("openAccount.account_type.document_discription.guest.item1") }}</p>
					<!-- <p>2) {{ $t("openAccount.account_type.document_discription.guest.item2") }}</p> -->
					<div class="my-8"></div>
					<p class="underline">{{ $t("openAccount.account_type.document_discription.juristic.title") }}</p>
					<p>1) {{ $t("openAccount.account_type.document_discription.juristic.item1") }}</p>
					<p>2) {{ $t("openAccount.account_type.document_discription.juristic.item2") }}</p>
					<p>3) {{ $t("openAccount.account_type.document_discription.juristic.item3") }}</p>
					<!-- <p>4) {{ $t("openAccount.account_type.document_discription.juristic.item4") }}</p>
					<p>5) {{ $t("openAccount.account_type.document_discription.juristic.item5") }}</p>
					<p>6) {{ $t("openAccount.account_type.document_discription.juristic.item6") }}</p> -->
					<div class="my-8"></div>
					<p class="underline">{{ $t("openAccount.account_type.document_discription.government.title") }}</p>
					<p>1) {{ $t("openAccount.account_type.document_discription.government.item1") }}</p>
					<p>2) {{ $t("openAccount.account_type.document_discription.government.item2") }}</p>
					<p>3) {{ $t("openAccount.account_type.document_discription.government.item3") }}</p>
					<!-- <p>4) {{ $t("openAccount.account_type.document_discription.government.item4") }}</p>
					<p>5) {{ $t("openAccount.account_type.document_discription.government.item5") }}</p> -->
				</div>
			</div>
		</div>
		<div class="w-full flex justify-center my-2">
			<button @click="$emit('click')" class="w-full md:w-4/12 bg-tgo-teal-500 border shadow-md rounded text-center py-2 text-white">{{ $t("button.confirm") }}</button>
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