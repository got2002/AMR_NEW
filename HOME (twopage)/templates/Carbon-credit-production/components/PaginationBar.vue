<template>
	<div>
		<div class="flex justify-end">
			<ul class="flex list-none rounded my-6 shadow-sm divide-x">
				<li class="text-sm relative block py-2 px-3 leading-tight bg-white cursor-pointer rounded-l" :title="$t('table.pagination.first_page')" @click="loadRequestByPage(1)">{{ $t("button.first_page") }}</li>
				<template v-for="n in meta.pages">
					<li :key="n" v-if="meta.pages > 1 && checkpage(n)" class="text-sm relative block py-2 px-3 leading-tight bg-white cursor-pointer" :class="{ 'bg-tgo-teal-500 text-white': n == meta.current_page, 'text-theme-black-200': n != meta.current_page }" :title="$t('table.pagination.page')" @click="loadRequestByPage(n)">{{ n }}</li>
					<li v-else-if="checkpage2(n)" :key="n + '.'" class="text-sm relative block py-2 px-3 leading-tight bg-white">.</li>
				</template>
				<li class="text-sm relative block py-2 px-3 leading-tight bg-white cursor-pointer rounded-r" :title="$t('table.pagination.last_page')" @click="loadRequestByPage(meta.pages)">{{ $t("button.last_page") }}</li>
			</ul>
		</div>
	</div>
</template>

<script>
export default {
	props: {
		meta: {
			type: Object,
			required: true,
		},
	},
	mounted() {
		// console.log(this.meta)
	},
	methods: {
		loadRequestByPage(page) {
			this.$emit("loadRequestByPage", parseInt(page));
		},
		checkpage(n) {
			if (Math.abs(this.meta.current_page - n) < 3 || Math.abs(this.meta.pages - n) < 3) {
				return true;
			} else {
				return false;
			}
		},
		checkpage2(n) {
			if (Math.abs(this.meta.current_page - n) < 4) {
				return true;
			} else {
				return false;
			}
		},
	},
};
</script>