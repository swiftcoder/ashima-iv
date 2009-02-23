{
	"version" : 1,
	
	"vertex" : {
		"source" : " \
			uniform mat4 model_view_matrix; \
			uniform mat3 model_view_normal_matrix; \
			uniform mat4 proj_matrix; \
			\
			void main() { \
				vec4 eye_pos = model_view_matrix * gl_Vertex; \
				vec3 eye_dir = model_view_normal_matrix * gl_Normal; \
				\
				vec3 dir = cross(eye_pos.xyz, eye_dir); \
				\
				eye_pos.xyz += normalize(dir); \
				\
				gl_Position = proj_matrix * eye_pos; \
				\
				gl_TexCoord[0] = gl_MultiTexCoord0; \
				}"
	},
	
	"fragment" : {
		"source" : " \
			uniform sampler2D tex0; \
			\
			void main() { \
				gl_FragColor = texture2D(tex0, vec2(gl_TexCoord[0].x, 0.0)) * (gl_TexCoord[0].y*0.6 + 0.4); \
			}"
	}
}
