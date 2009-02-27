{
	"version" : 1,
	
	"vertex" : {
		"source" : " \
			uniform mat4 model_view_proj_matrix; \
			\
			varying vec4 colour; \
			\
			void main() { \
				gl_Position = model_view_proj_matrix * gl_Vertex; \
				\
				gl_TexCoord[0] = gl_MultiTexCoord0; \
				colour = gl_Color; \
				}"
	},
	
	"fragment" : {
		"source" : " \
			uniform sampler2D tex0; \
			\
			varying vec4 colour; \
			\
			void main() { \
				gl_FragColor = colour * texture2D(tex0, gl_TexCoord[0].xy); \
			}"
	}
}
