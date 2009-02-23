{
	"version" : 1,
	
	"vertex" : {
		"source" : " \
			uniform mat4 model_view_proj_matrix; \
			uniform mat4 model_view_matrix; \
			\
			void main() { \
				gl_Position = model_view_proj_matrix * gl_Vertex; \
				\
				//vec4 eye = model_view_matrix * gl_Vertex; \
				//float d = length(eye.xyz); \
				//gl_PointSize = 128.0 * sqrt( 1.0/(1.0 + d*d) ); \
				gl_PointSize = 10.0 * gl_MultiTexCoord1.x; \
				\
				gl_TexCoord[0] = gl_MultiTexCoord0; \
				gl_TexCoord[1] = gl_MultiTexCoord1; \
				}"
	},
	
	"fragment" : {
		"source" : " \
			uniform sampler2D tex0; \
			\
			void main() { \
				//gl_FragColor = gl_TexCoord[0]; \
				gl_FragColor = texture2D(tex0, gl_TexCoord[0].xy); // * vec4(1.0, 1.0, 1.0, gl_TexCoord[1].x); \
			}"
	}
}
