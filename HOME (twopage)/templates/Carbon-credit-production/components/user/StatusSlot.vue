<template>
	<td
		class="border-t-0 px-1 whitespace-nowrap align-center"
		:class="{
			'text-left': align === 'left',
			'text-center': align === 'center',
			'text-right': align === 'right',
		}"
	>
		<span class="px-3 py-1 rounded-full" :class="{
            'bg-yellow-100 bg-opacity-40 border border-yellow-500 text-yellow-500':status === 0,
            'bg-green-100 bg-opacity-40 border border-green-500 text-green-500':status === 1,
            'bg-red-100 bg-opacity-40 border border-red-500 text-red-500':status === 2,
          

        

        }">
			{{ statusText(status) }}
		</span>
	</td>
</template>

<script>
	export default {
        props:['status','align'],
        methods:{
            statusText(status){
                switch (status) {
                    case 0:
                        if(this.$i18n.locale === 'th') return 'รอยืนยัน'
                        else return 'pending'
                    case 1:
                        if(this.$i18n.locale === 'th') return 'ยืนยันแล้ว'
                        else return 'approved'
                    case 2:
                        if(this.$i18n.locale === 'th') return 'ปฏิเสธ'
                        else return 'rejected'
                
                    default:
                        break;
                }
            }
        }
    };
</script>

<style></style>
