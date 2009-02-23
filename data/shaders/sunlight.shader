{
	"version" : 1,
	
	"vertex" : {
		"source" : " \
			uniform mat4 model_view_proj_matrix; \
			uniform mat3 inv_model_normal_matrix; \
			uniform vec3 sunDir; \
			\
			varying vec3 sun; \
			\
			void main() { \
				gl_Position = model_view_proj_matrix * gl_Vertex; \
				sun = normalize(inv_model_normal_matrix * sunDir); \
				\
				gl_TexCoord[0] = gl_MultiTexCoord0; \
				}"
	},
	
	"fragment" : {
		"source" : " \
			uniform sampler2D tex0, tex1; \
			\
			varying vec3 sun; \
			\
			void main() { \
				vec4 texture = texture2D(tex0, gl_TexCoord[0].xy); \
				vec3 normal = texture2D(tex1, gl_TexCoord[0].xy).xyz; \
				\
				float diffuse = dot( normal, sun ); \
				float specular = 4.0*pow(diffuse, 32.0); \
				\
				gl_FragColor = (diffuse + specular + 0.25)*texture; \
			}"
	}
}
