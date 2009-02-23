{
	"version" : 1,
	
	"vertex" : {
		"source" : " \
			uniform mat4 model_view_proj_matrix; \
			\
			void main() { \
				gl_Position = model_view_proj_matrix * gl_Vertex; \
			}"
	},
	
	"fragment" : {
		"source" : " \
			void main() { \
				gl_FragColor = vec4(1.0); \
			}"
	}
}
