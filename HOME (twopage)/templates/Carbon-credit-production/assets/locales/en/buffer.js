export default {
    page_title: "Buffer data",
    tab:{
		buffer:'Buffer list',
		reversal:'Reversal retirement list'
	},
    table:{
        project_id:'Project Id',
        project_name:'Project Name',
        vintage:'Vintage',
        buffer:'Buffer',
        endDate:'End Date',
        createdAt:'Retired At',
        tool:'Tools'
    },
    modal: {
        title: "Issue",
        title2: "Reversal retirement",
		subtitle: "Total buffer {amount} tCO2eq",

		remark: "Remark",
		buffer: "Buffer",
        issue:'Issue',
        reversal:'Reversal retirement',
        total:'Total',
       

		placeholder_remark: "Type your message here...",

		validation: {
			required: "Required",
			specification: "Please specific buffer percentage to issue carbon",
			specification2: "Please specific percentage of reversal retirement",
		},

    }
}