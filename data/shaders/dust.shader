{
	"version" : 1,
	
	"vertex" : {
		"source" : " \
			uniform mat4 model_view_proj_matrix; \
			\
			varying float depth; \
			\
			void main() { \
				gl_Position = model_view_proj_matrix * gl_Vertex; \
				depth = gl_Position.z; \
				gl_PointSize = 4.0; \
			}"
	},
	
	"fragment" : {
		"source" : " \
			varying float depth; \
			\
			void main() { \
				//float fog = (gl_Fog.end - gl_FogFragCoord) * gl_Fog.scale; \
				//gl_FragColor = mix(gl_Fog.color, vec4(1.0), fog); \
				float fog = (10.0 - depth) * 5.0; \
				gl_FragColor = mix(vec4(0.0), vec4(1.0), fog); \
			}"
	}
}
