`ifndef _VGA_
`define _VGA_

module vga #(
    parameter H_RES = 1280,
    H_FRONT_PORCH = 48,
    H_SYNC_PULSE = 112,
    H_BACK_PORCH = 248,
    V_RES = 1024,
    V_FRONT_PORCH = 1,
    V_SYNC_PULSE = 3,
    V_BACK_PORCH = 38
)(
	input clk_108Mhz,
	output h_sync,
	output v_sync,
	output  [10:0] x_loc,
    output  [10:0] y_loc
);   

    localparam H_TOTAL = H_RES+H_FRONT_PORCH+H_SYNC_PULSE+H_BACK_PORCH-1;
    
	h_sync #(
        .H_RES(H_RES),
        .H_FRONT_PORCH(H_FRONT_PORCH),
        .H_SYNC_PULSE(H_SYNC_PULSE),
        .H_BACK_PORCH(H_BACK_PORCH)
	) horizontal (
		.clk(clk_108Mhz),
		.h_sync_signal(h_sync),
		.h_sync_counter(x_loc)
	);

	v_sync # (
	    .V_RES(V_RES),
        .V_FRONT_PORCH(V_FRONT_PORCH),
        .V_SYNC_PULSE(V_SYNC_PULSE),
        .V_BACK_PORCH(V_BACK_PORCH),
        .H_LIMIT(H_TOTAL)
	) vertical (
		.clk(clk_108Mhz),
		.x_location(x_loc),
		.v_sync_signal(v_sync),
		.v_sync_counter(y_loc)
	);
endmodule
`endif
