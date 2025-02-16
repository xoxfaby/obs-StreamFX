// AUTOGENERATED COPYRIGHT HEADER START
// Copyright (C) 2018-2023 Michael Fabian 'Xaymar' Dirks <info@xaymar.com>
// AUTOGENERATED COPYRIGHT HEADER END

#pragma once
#include "common.hpp"
#include "obs/gs/gs-texrender.hpp"
#include "obs/gs/gs-texture.hpp"
#include "obs/obs-source.hpp"
#include "obs/obs-weak-source.hpp"

#include "warning-disable.hpp"
#include <map>
#include "warning-enable.hpp"

namespace streamfx::gfx {
	class source_texture {
		streamfx::obs::source _parent;
		streamfx::obs::source _child;

		std::shared_ptr<streamfx::obs::gs::texrender> _rt;

		public:
		~source_texture();
		source_texture(streamfx::obs::source child, streamfx::obs::source parent);

		public /*copy*/:
		source_texture(source_texture const& other)            = delete;
		source_texture& operator=(source_texture const& other) = delete;

		public /*move*/:
		source_texture(source_texture&& other)            = delete;
		source_texture& operator=(source_texture&& other) = delete;

		public:
		std::shared_ptr<streamfx::obs::gs::texture> render(std::size_t width, std::size_t height);

		public: // Unsafe Methods
		void clear();

		obs_source_t* get_object();
		obs_source_t* get_parent();
	};
} // namespace streamfx::gfx
