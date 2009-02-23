{
	"version" : 1,
	
	"vertex" : {
		"source" : " \
			uniform mat4 model_view_proj_matrix; \
			\
			void main() { \
				gl_Position = model_view_proj_matrix * gl_Vertex; \
				\
				gl_TexCoord[0] = gl_MultiTexCoord0; \
				}"
	},
	
	"fragment" : {
		"source" : " \
			uniform sampler2D tex0; \
			\
			void main() { \
				gl_FragColor = texture2D(tex0, gl_TexCoord[0].xy); \
			}"
	}
}
